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
    indicators = _check_indicators(indicators)
    if _is_cached(ticker, timeframe, start_date, end_date, indicators, shift):
        data = _load_cached_data(ticker, timeframe, start_date, end_date,
                                 indicators, shift)
    else:
        data = _load_data_given_dates(ticker, timeframe, start_date, end_date,
                                      indicators, shift)
    if cache:
        _cache_data(data, filename, ticker, timeframe, shift)
    if not reverse:
        data = data[::-1]
    data = _rename_columns(data)
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
    filename = _get_filename(ticker, timeframe, start_date, end_date, shift)
    list_of_ind_names = list(indicators.keys())
    indicators = _check_indicators(indicators)
    if _is_cached(ticker, timeframe, start_date, end_date, indicators, shift):
        data = _load_cached_data(ticker, timeframe, start_date, end_date,
                                 indicators, shift)
    else:
        data, ind_str = _load_data_given_dates(ticker, timeframe, start_date, end_date,
                                      indicators, shift)
    if cache:
        _cache_data(data, ind_str, filename, ticker, timeframe, shift)
    if not reverse:
        data = data[::-1]
    return data


def _get_filename(ticker, timeframe, start_date, end_date, shift):
    start_date_str = start_date.strftime("%Y%m%d%H%M%S")
    end_date_str = end_date.strftime("%Y%m%d%H%M%S")
    filename = "__" + ticker + str(timeframe)\
                +"_s"+str(shift) + "_" \
                + start_date_str + "_" \
                + end_date_str + "__"
    return filename


def _get_cached_file(ticker, timeframe, shift=None):
    start_string = "__" + ticker + str(timeframe) + "_s"
    if shift is not None and isinstance(shift, int):
        start_string += str(shift)
    cached_file = [
        file_ for file_ in os.listdir(where_to_cache)
        if os.path.isfile((os.path.join(where_to_cache, file_)))
        and file_.startswith(start_string)
    ]
    if cached_file:
        return cached_file[0]
    else:
        return False


def _get_cached_dates(ticker, timeframe, shift):
    cached_file = _get_cached_file(ticker, timeframe, shift)
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


def _load_cached_data(ticker, timeframe, start_date, end_date, indicators=None,
                      shift=0):
    def dict_to_list(ind_dict):
        ret_list = list()
        for ind_name in ind_dict.values():
            if isinstance(ind_name, str):
                ind = ind_name
            elif isinstance(ind_name, tuple):
                ind = ind_name[0]
        ret_list.append(ind)
        return ret_list

    start_date_, end_date_ = _get_cached_dates(ticker, timeframe, shift)
    if start_date > start_date_:
        start_date_ = start_date
    if end_date < end_date_:
        end_date_ = end_date
    start_date_int = int(start_date_.strftime("%Y%m%d%H%M%S"))
    end_date_int = int(end_date_.strftime("%Y%m%d%H%M%S"))
    cached_file = _get_cached_file(ticker, timeframe)
    data = pd.read_csv(where_to_cache + cached_file, index_col=False)
    data = data[data['time'].between(
        start_date_int, end_date_int, inclusive=True)]
    replace_ind, add_ind = _find_uncached_indicators(cached_file, indicators,
                                                     0)
    for ind_name in replace_ind.keys():
        inds_to_delete = [
            elem for elem in list(data) if elem.startswith(ind_name)
        ]
        data = data.drop(inds_to_delete, axis=1)
    if indicators is not None:
        for ind_name in indicators.keys():
            ind = ind_name[0]
            if ind in replace_ind.keys():
                add_ind.update({ind_name: indicators[ind_name]})
        if add_ind:
            add_data = _load_data_given_dates(ticker, timeframe, start_date_,
                                            end_date_, add_ind, shift)
            add_data = add_data.drop(
                ['time', 'open', 'high', 'low', 'close', 'vol'], axis=1)
            data = pd.concat([data, add_data], axis=1)
            data = data[list(data)[:6] + sorted(list(data)[6:])]
        for col in data.columns[6:]:
            col_ = col.split("_")[0]
            if not any(col_.startswith(key) for key in dict_to_list(indicators)):
                data.drop(columns=[col], inplace=True)
    return data


def _find_uncached_data(ticker, timeframe, start_date, end_date):
    uncached_data = list()
    cached_dates = _get_cached_dates(ticker, timeframe)
    if cached_dates is not None:
        if start_date < cached_dates[0]:
            uncached_data.append((start_date, cached_dates[0]))
        if end_date > cached_dates[1]:
            uncached_data.append((cached_dates[1], end_date))
    else:
        uncached_data.append((start_date, end_date))
    return uncached_data


def _load_data_given_dates(
        ticker, timeframe, start_date, end_date, indicators=None, shift=0
    ):
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
            l = [item.split(".")[1] for item in ind_values if len(item.split(".")) > 1]
            if l:
                for key in ind_values.keys():
                    dict_values[ind_key+"."+key.split(".")[1]] = ind_values[key]
            else:
                dict_values[ind_key] = ind_values[list(ind_values.keys())[0]]

            explanatory_str = ""
            for param in ind_params:
                explanatory_str += "_" + str(param)
            for key in ind_values.keys():
                ind_names_string.append(key + explanatory_str)
            key+explanatory_str
            rates = pd.concat([rates, pd.DataFrame.from_dict(dict_values)], axis=1)
    return rates, ind_names_string


def _rename_columns(data):
    to_rename = dict.fromkeys(data.columns[6:])
    for column_name in data.columns[6:]:
        to_rename[column_name] = column_name.split('_')[0]
    data.rename(columns=to_rename, inplace=True)
    return data


def _is_cached(ticker, timeframe, start_date, end_date, indicators, shift):
    cached_file = _get_cached_file(ticker, timeframe, shift)
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


def _cache_data(data, ind_str, filename, ticker, timeframe, shift):
    already_cached = _get_cached_file(ticker, timeframe, shift)
    renamed_data = data.rename(columns=dict(zip(list(data.columns), ind_str)))
    if already_cached:
        os.remove(where_to_cache + already_cached)
        renamed_data.to_csv(where_to_cache + filename, index=False, mode="a")
    else:
        renamed_data.to_csv(where_to_cache + filename, index=False, mode="a")


def _find_uncached_indicators(cached_file, indicators, check):
    data_file = pd.read_csv(where_to_cache + cached_file)
    ind_dict = _indicators_to_dict(list(data_file)[6:])
    replace_ind = dict()
    add_ind = dict()
    if indicators is not None:
        for ind_header in indicators.values():
            ind_name = ind_header[0]
            ind_params = ind_header[1:]
            if ind_name not in ind_dict.keys():
                add_ind[ind_name] = ind_params
            else:
                if ind_dict[ind_name] != ind_params:
                    replace_ind[ind_name] = ind_dict[ind_name]
    if check:
        for ind in ind_dict.keys():
            if ind not in indicators.keys():
                add_ind[ind] = ind_dict[ind]
    return replace_ind, add_ind


def _get_inds_for_aux_dates(cached_file, indicators):
    data_file = pd.read_csv(where_to_cache + cached_file)
    ind_dict = _indicators_to_dict(list(data_file)[6:])
    replace, add = _find_uncached_indicators(cached_file, indicators, 0)
    new_inds = dict()
    for ind in replace.keys():
        if ind in ind_dict.keys():
            ind_dict.pop(ind)
            ind_dict[ind] = indicators[ind]
    ind_dict.update(add)
    return ind_dict


def _indicators_to_dict(indicators):
    print(indicators)
    input("")
    ind_dict = dict()
    for ind in indicators:
        splitted_ind = ind.split("_")
        ind_name = splitted_ind[0].split(".")[0]
        ind_params = (splitted_ind[1:])
        if ind_name not in ind_dict.keys():
            if len(ind_params) > 1:
                ind_params[0] = int(ind_params[0])
                ind_dict[ind_name] = tuple(ind_params)
            elif len(ind_params) == 1:
                ind_dict[ind_name] = int(ind_params[0])
            else:
                ind_dict[ind_name] = ()
    return ind_dict


def _check_indicators(indicators):
    to_str = lambda x: (x,) if isinstance(x, str) else x
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