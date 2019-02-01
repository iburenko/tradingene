import sys
import os
from datetime import datetime, timedelta
import time
import numpy as np
import pandas as pd
from tradingene.algorithm_backtest.tng import TNG
from tradingene.data.data import Data
from tradingene.data.data_separation import separate_data
import tradingene.ind.ind as tngind
from tradingene.data.date_init import moex_start_date, moex_end_date
from tradingene.algorithm_backtest.limits import moex_tickers

dt = np.dtype({
    'names': ['time', 'open', 'high', 'low', 'close', 'vol'],
    'formats':
    ['uint64', 'float64', 'float64', 'float64', 'float64', 'float64']
})

where_to_cache = os.path.dirname(
    os.path.abspath(__file__)) + '/__cached_history__/'


def import_data(ticker,
                timeframe,
                start_date,
                end_date,
                calculate_input=None,
                lookback=None,
                calculate_output=None,
                lookforward=None,
                reverse=True,
                split=(50, 25, 25),
                indicators=None,
                cache=True,
                shift=0,
                bootstrap=0):
    if not isinstance(ticker, str) or \
        not isinstance(timeframe, int) or \
        not isinstance(start_date, datetime) or \
        not isinstance(end_date, datetime) or \
        not isinstance(split, tuple) \
        or len(split) > 3 or len(split) < 2:
        raise TypeError("Check types of arguments!")
    if sum(split) != 100:
        raise ValueError("Sum of values in split must be 100!")
    if not callable(calculate_input) and calculate_input is not None:
        raise TypeError("calculate_input must be callable or None!")
    if not callable(calculate_output) and calculate_output is not None:
        raise TypeError("calculate_output must be callable or None!")
    if not isinstance(lookback, int):
        raise TypeError("lookback must be int!")
    elif lookback < 1:
        raise ValueError("lookback must be positive!")
    if not isinstance(lookforward, int):
        raise TypeError("lookforward must be int!")
    elif lookforward < 1:
        raise ValueError("lookforward must be positive!")

    check_home_folder()
    delete_old_files()
    filename = _get_filename(ticker, timeframe, start_date, end_date, shift)
    if indicators:
        indicators = _check_indicators(indicators)
    if _is_cached(ticker, timeframe, start_date, end_date, shift):
        data, ind_str = _load_cached_data(ticker, timeframe, start_date,
                                          end_date, indicators, shift)
    else:
        data, ind_str = _load_data_given_dates(ticker, timeframe, start_date,
                                               end_date, indicators, shift)
    if cache:
        _cache_data(data, ind_str, filename, ticker, timeframe, start_date, end_date, shift)
    if not reverse:
        data = data[::-1].reset_index(drop=True)
    return separate_data(data, split, calculate_input, calculate_output,
                         lookback, lookforward, bootstrap)


def import_candles(ticker,
                   timeframe,
                   start_date,
                   end_date,
                   reverse=True,
                   indicators=None,
                   cache=True,
                   shift=0):
    if not isinstance(ticker, str) or \
        not isinstance(timeframe, int) or \
        not isinstance(start_date, datetime) or \
        not isinstance(end_date, datetime):
        raise TypeError("Check types of arguments!")

    check_home_folder()
    delete_old_files()
    
    if indicators:
        indicators = _check_indicators(indicators)
    if ticker in moex_tickers:
        start_date, end_date = moex_start_date(start_date), moex_end_date(end_date)
    filename = _get_filename(ticker, timeframe, start_date, end_date, shift)
    if _is_cached(ticker, timeframe, start_date, end_date, shift):
        data, ind_str = _load_cached_data(ticker, timeframe, start_date,
                                          end_date, indicators, shift)
    else:
        data, ind_str = _load_data_given_dates(ticker, timeframe, start_date,
                                               end_date, indicators, shift)
    if cache:
        _cache_data(data, ind_str, filename, ticker, timeframe, start_date, end_date, shift)
    if not reverse:
        data = data[::-1].reset_index(drop=True)
    return data


def _load_cached_data(ticker,
                      timeframe,
                      start_date,
                      end_date,
                      indicators=None,
                      shift=0):
    start_date_, end_date_ = _get_cached_dates(ticker, timeframe, start_date, end_date, shift)
    if start_date > start_date_:
        start_date_ = start_date
    if end_date < end_date_:
        end_date_ = end_date
    start_date_int = int(start_date_.strftime("%Y%m%d%H%M%S"))
    end_date_int = int(end_date_.strftime("%Y%m%d%H%M%S"))
    cached_file = _get_cached_file(ticker, timeframe, start_date, end_date, shift)
    data = pd.read_csv(where_to_cache + cached_file, index_col=False)
    data = data[data['time'].between(
        start_date_int, end_date_int, inclusive=True)]
    to_add, old_inds, to_delete = _find_uncached_indicators(
        list(data), indicators)
    data = delete_unneeded_indicators(data, to_delete)
    data = rename_columns(data, indicators)
    inds_to_load = load_new_indicators(data, indicators, to_add) if to_add else None
    if inds_to_load:
        add_data, add_data_str = _load_data_given_dates(
            ticker, timeframe, start_date_, end_date_, inds_to_load, shift)
        add_data.drop(
            ['time', 'open', 'high', 'low', 'close', 'vol'],
            axis=1,
            inplace=True)
        data = pd.concat([data, add_data], axis=1)
    return data, convert_indnames(data, indicators)


def _load_data_given_dates(ticker,
                           timeframe,
                           start_date,
                           end_date,
                           indicators=None,
                           shift=0):
    """ Loads data in the given time period

        Returns: 

        data (pandas' DataFrame): Columns of this
        DataFrame correponds to the names of indicators
        given by a user.

        ind_names_string (list): list of names used for
        storing calculated data on a drive. Uses values
        from a user's dict that defines indicators.

        Example: inds = {'my_macd': ('macd', 5), 'ema': ('ema', 10)}
        list(data)[6:] is [
            'my_macd.macd', my_macd.signal', 'my_macd.histogram', 'ema'
            ]
        ind_names_string is [
            'macd_5.macd, 'macd_5.signal', 'macd_5.histogram', 'ema_10'
            ]
    """

    end_date += timedelta(minutes=1 + shift)
    start_date += timedelta(minutes=shift)
    data = Data.load_data(ticker, start_date, end_date)
    data = data[::-1]
    data['time'] = pd.to_datetime(data['time'], format="%Y%m%d%H%M%S")
    td = end_date - start_date
    days, seconds = td.days, td.seconds
    iters = (days * 1440 + seconds // 60) // timeframe
    ind = 0
    rates = np.empty(iters, dtype=dt)
    for i in range(iters):
        candle_data = data[data['time'].between(
            start_date + i * timedelta(minutes=timeframe),
            start_date + (i + 1) * timedelta(minutes=timeframe) -
            timedelta(minutes=1))]
        try:
            rates[ind] = (int(
                candle_data['time'].iloc[0].strftime("%Y%m%d%H%M%S")),
                          candle_data['open'].iloc[0], max(
                              candle_data['high']), min(candle_data['low']),
                          candle_data['close'].iloc[-1], sum(
                              candle_data['vol']))
            ind += 1
        except:
            pass
    if ind - iters < 0:
        rates = rates[:ind - iters]
    rates = pd.DataFrame(rates[::-1])
    ind_names_string = list(rates.columns)
    if indicators is not None:
        for ind_key, ind_header in indicators.items():
            ind_name = ind_header[0]
            ind_params = ind_header[1:]
            for class_name in dir(tngind):
                if ind_name == class_name[3:].lower():
                    break
            new_ind = eval("tngind." + class_name + str(ind_params))
            ind_values = new_ind.calculateRates(rates)

            dict_values = dict()
            l = [
                item.split(".")[1] for item in ind_values
                if len(item.split(".")) > 1
            ]
            if l:
                for key in ind_values.keys():
                    dict_values[ind_key + "." +
                                key.split(".")[1]] = ind_values[key]
            else:
                dict_values[ind_key] = ind_values[list(ind_values.keys())[0]]

            explanatory_str = ""
            for param in ind_params:
                explanatory_str += "_" + str(param)
            for key in ind_values.keys():
                dot_splitted = key.split(".")
                if len(dot_splitted) == 1:
                    ind_names_string.append(key + explanatory_str)
                else:
                    ind_names_string.append(dot_splitted[0] + explanatory_str +
                                            "." + dot_splitted[1])
            rates = pd.concat(
                [rates, pd.DataFrame.from_dict(dict_values)], axis=1)
    # if shift:
    #     rates = rates[:-1]
    return rates, ind_names_string


def _is_cached(ticker, timeframe, start_date, end_date, shift):
    """ Whether data were cached.

        Returns: False -- if there is not file with data
                 False -- if cached start_date > required start_date
                 False -- if cached end_date < required end_date
                 True -- otherwise
    """

    cached_file = _get_cached_file(ticker, timeframe, start_date, end_date, shift)
    if not cached_file:
        return False
    cached_file = cached_file.replace("__", "")
    cached_file = cached_file.replace(ticker + str(timeframe) + "_", "")
    shift_and_dates = cached_file.split("_")
    cached_shift = int(shift_and_dates[0][1:])
    start_date_str = shift_and_dates[1]
    end_date_str = shift_and_dates[2]
    prev_start_date = \
                datetime(*(time.strptime(start_date_str, "%Y%m%d%H%M%S")[0:6]))
    prev_end_date = \
                datetime(*(time.strptime(end_date_str, "%Y%m%d%H%M%S")[0:6]))
    if prev_start_date > start_date:
        return False
    elif prev_end_date < end_date:
        return False
    elif cached_shift != shift:
        return False
    else:
        return True


def _cache_data(data, ind_str, filename, ticker, timeframe, start_date, end_date, shift):
    already_cached = _get_cached_file(ticker, timeframe, start_date, end_date, shift)
    renamed_data = data.rename(columns=dict(zip(list(data.columns), ind_str)))
    if already_cached:
        renamed_data.to_csv(where_to_cache + filename, index=False)
    else:
        renamed_data.to_csv(where_to_cache + filename, index=False)


def _find_uncached_indicators(saved_indicators, indicators):
    loaded_dict = {item.split(".")[0] for item in saved_indicators[6:]}
    ind_dict = set()
    if indicators:
        for value in indicators.values():
            exp_str = value[0]
            for param in value[1:]:
                if len(value) > 1 and not isinstance(value[1], int):
                    raise TypeError("")
                exp_str += "_" + str(param)
            ind_dict.add(exp_str)
    return ind_dict - loaded_dict, ind_dict & loaded_dict, loaded_dict - ind_dict


def _check_indicators(indicators):
    to_str = lambda x: (x, ) if isinstance(x, str) else x
    return {key: to_str(indicators[key]) for key in indicators.keys()}


def check_home_folder():
    home_folder = os.path.dirname(os.path.abspath(__file__))
    if '__cached_history__' not in os.listdir(home_folder):
        os.mkdir(home_folder + '/__cached_history__/')


def delete_old_files():
    cached_files = [
        file_ for file_ in os.listdir(where_to_cache) if os.path.isfile((
            os.path.join(where_to_cache, file_))) and file_.startswith('__')
    ]
    for file_ in cached_files:
        timestamp = os.path.getmtime(where_to_cache + file_)
        this_moment = datetime.now()
        if (this_moment - datetime.fromtimestamp(timestamp)).days > 31:
            os.remove(where_to_cache + file_)


def delete_unneeded_indicators(data, new_ind):
    to_del = [elem for elem in data if any(elem.startswith(item) for item in new_ind)]
    data.drop(columns=to_del, inplace=True)
    return data


def load_new_indicators(data, indicators, new_ind):
    new_dict = None
    if indicators:
        new_ind_tuple = list()
        for elem in new_ind:
            splitted = elem.split("_")
            if len(splitted) > 1:
                splitted[1] = int(splitted[1])
            new_ind_tuple.append(tuple(splitted))
        new_dict = {
            key: value
            for key, value in indicators.items() if value in new_ind_tuple
        }
    return new_dict


def rename_columns(data, indicators):
    rename_dict = dict()
    for ind_name in list(data)[6:]:
        splitted_name = ind_name.split(".")
        ind_key = _get_vocab_key_by_value(indicators, splitted_name[0])
        converted = ind_key + "." + splitted_name[1] if len(splitted_name) > 1 else ind_key
        rename_dict.update({ind_name:converted})
        rename_dict
    data.rename(columns=rename_dict, inplace=True)
    return data


def convert_indnames(data, indicators):
    converted_list = list(data)[:6]
    if indicators:
        for ind_name in list(data)[6:]:
            splitted_name = ind_name.split(".")
            new_name = indicators[splitted_name[0]][0]
            explanatory_str = ""
            for param in indicators[splitted_name[0]][1:]:
                explanatory_str += "_" + str(param)
            new_name += explanatory_str
            converted = new_name + "." + splitted_name[1] if len(splitted_name) > 1 else new_name
            converted_list.append(converted)
    return converted_list


def _get_filename(ticker, timeframe, start_date, end_date, shift):
    start_date_str = start_date.strftime("%Y%m%d%H%M%S")
    end_date_str = end_date.strftime("%Y%m%d%H%M%S")
    filename = "__" + ticker + str(timeframe)\
                +"_s"+str(shift) + "_" \
                + start_date_str + "_" \
                + end_date_str + "__"
    return filename


def _get_cached_file(ticker, timeframe, start_date, end_date, shift):
    start_string = "__" + ticker + str(timeframe) + "_s"
    if shift is not None and isinstance(shift, int):
        start_string += str(shift)
    start_string += str(start_date)+"_"+str(end_date)
    cached_file = [
        file_ for file_ in os.listdir(where_to_cache)
        if os.path.isfile((os.path.join(where_to_cache, file_)))
        and file_.startswith(start_string)
    ]
    if cached_file:
        return cached_file[0]
    else:
        return False


def _get_cached_dates(ticker, timeframe, start_date, end_date, shift):
    cached_file = _get_cached_file(ticker, timeframe, start_date, end_date, shift)
    if not cached_file:
        return None
    replaced_filename = cached_file.replace("0__", "0")
    start_string = "__" + ticker + str(timeframe) + "_"
    dates = replaced_filename.replace(start_string, "").split("_")
    start_date_str = dates[1]
    end_date_str = dates[2]
    prev_start_date = \
                datetime(*(time.strptime(start_date_str, "%Y%m%d%H%M%S")[0:6]))
    prev_end_date = \
                datetime(*(time.strptime(end_date_str, "%Y%m%d%H%M%S")[0:6]))
    return prev_start_date, prev_end_date


def _get_vocab_key_by_value(indicators, value):
    ind_params = value.split("_")
    if len(ind_params) == 1:
        ind_value = tuple(ind_params, )
    if len(ind_params) >= 2:
        ind_params[1] = int(ind_params[1])
        ind_value = tuple(ind_params)
    for key, value in indicators.items():
        if value == ind_value:
            return key


