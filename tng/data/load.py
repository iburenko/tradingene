import sys
import os
from datetime import datetime
import time
import numpy as np
import pandas as pd
from tng.algorithm_backtest.tng import TNG

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
                calculate_input = None,
                lookback = None,
                calculate_output = None,
                lookforward = None,
                reverse=True,
                split=(50, 25, 25),
                indicators=None,
                cache=True,
                shift=0):
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
    filename = _filename(ticker, timeframe, start_date, end_date)
    _check_cached_data(ticker, timeframe, start_date, end_date)
    if _is_cached(filename):
        data = pd.read_csv(where_to_cache + filename, index_col=False)
    else:
        data = _load_data(ticker, timeframe, start_date, end_date, indicators)
        if cache:
            _cache_data(data, filename, shift)
    if not reverse:
        data = data[::-1]
    return separate_data(data, split, calculate_input, calculate_output,
                        lookback, lookforward)

def import_candles(ticker,
                timeframe,
                start_date,
                end_date,
                reverse=True,
                indicators=None,
                cache=True,
                shift=0):
    check_home_folder()
    delete_old_files()
    filename = _filename(ticker, timeframe, start_date, end_date)
    if _is_cached(filename):
        data = pd.read_csv(where_to_cache + filename, index_col=False)
    else:
        check_cached_data(ticker, timeframe, start_date, end_date)
        data = _load_data(ticker, timeframe, start_date, end_date, indicators, shift)
        if cache:
            _cache_data(data, filename, shift)
    if not reverse:
        data = data[::-1]
    return data

def _load_data(ticker, timeframe, start_date, end_date, indicators, shift = 0):
    data_columns = ['time', 'open', 'high', 'low', 'close', 'vol']
    sample = np.empty(len(data_columns))
    data = np.array([])
    ind_dict = dict()

    def on_bar(instrument):
        nonlocal data, ind_dict
        sample[0:6] = instrument.time,\
                    instrument.open[1], \
                    instrument.high[1],\
                    instrument.low[1],\
                    instrument.close[1],\
                    instrument.vol[1]
        i = 6
        if indicators:
            for key, params in indicators.items():
                if not isinstance(params, tuple):
                    params = (params, )
                ind = eval("instrument." + str(key))
                parsed = _parse_indicator(key, ind(*params))
                for key, value in parsed.items():
                    if key in ind_dict.keys():
                        ind_dict[key].append(value)
                    else:
                        ind_dict[key] = [value]
        data = np.append(data, sample)

    name = "import_data"
    regime = "SP"
    alg = TNG(name, regime, start_date, end_date)
    alg.addInstrument(ticker)
    alg.addTimeframe(ticker, timeframe)
    alg.run_backtest(on_bar, shift)
    del alg
    data = np.reshape(data,
                      (len(data) // len(data_columns), len(data_columns)))
    data = pd.DataFrame(data, columns=data_columns)
    data = pd.concat([data, pd.DataFrame.from_dict(ind_dict)], axis=1)
    return data


def _filename(ticker, timeframe, start_date, end_date):
    start_date_str = start_date.strftime("%Y%m%d%H%M%S")
    end_date_str = end_date.strftime("%Y%m%d%H%M%S")
    filename = "__" + ticker + str(
        timeframe) + "_" + start_date_str + "_" + end_date_str + "__"
    return filename


def _check_cached_data(ticker, timeframe, start_date, end_date):
    start_string = '__'+ticker+str(timeframe)+"_"
    cached_file = [
        file_ for file_ in os.listdir(where_to_cache) if os.path.isfile((
        os.path.join(where_to_cache, file_))) and file_.startswith(start_string)
    ]
    dates = cached_file[0].replace(start_string, "").split("_")
    start_date_str = dates[0]
    end_date_str = dates[1]
    prev_start_date = \
                datetime(*(time.strptime(start_date_str, "%Y%m%d%H%M%S")[0:6]))
    prev_end_date = \
                datetime(*(time.strptime(end_date_str, "%Y%m%d%H%M%S")[0:6]))
    
    

def separate_data(data, split, calculate_input, calculate_output, lookback,
                  lookforward):
    data = data.to_records()
    split_data = dict()
    input_parameters = np.empty([])
    output_parameters = np.empty([])
    for i in range(lookback, len(data) - lookforward - 1):
        inp = np.array([calculate_input(data[i - lookback:i + 1][::-1])])
        out = np.array([calculate_output(data[i:i + lookforward + 1])])
        input_parameters = np.append(input_parameters, inp)
        output_parameters = np.append(output_parameters, out)
    input_parameters = np.delete(input_parameters, 0)
    output_parameters = np.delete(output_parameters, 0)
    input_len = len(input_parameters)
    input_parameters = np.reshape(input_parameters,
                                  (input_len // inp.shape[-1], inp.shape[-1]))
    if len(split) == 2:
        train_len = input_parameters.shape[0] * split[0] // 100
        split_data['train_input'] = input_parameters[1:train_len]
        split_data['train_output'] = output_parameters[1:train_len]
        split_data['test_input'] = input_parameters[train_len:]
        split_data['test_output'] = output_parameters[train_len:]
    elif len(split) == 3:
        train_len = input_parameters.shape[0] * split[0] // 100
        validation_len = input_parameters.shape[0] * split[1] // 100
        split_data['train_input'] = input_parameters[0:train_len]
        split_data['train_output'] = output_parameters[0:train_len]
        split_data['validation_input'] = input_parameters[train_len:train_len +
                                                          validation_len]
        split_data['validation_output'] = output_parameters[
            train_len:train_len + validation_len]
        split_data['test_input'] = input_parameters[train_len +
                                                    validation_len:]
        split_data['test_output'] = output_parameters[train_len +
                                                      validation_len:]
    return split_data


def _parse_indicator(ind_name, ind_value):
    if isinstance(ind_value, list):
        ret_dict = dict.fromkeys([ind_name])
        ret_dict[ind_name] = ind_value[1]
    else:
        keys = [
            ind_name + "." + str(elem) for elem in ind_value.__dict__.keys()
        ]
        ret_dict = dict.fromkeys(keys)
        for key, value in (ind_value.__dict__.items()):
            ret_dict[ind_name + "." + key] = value[1]
    return ret_dict


def _is_cached(filename):
    cached_files = [
        file_ for file_ in os.listdir(where_to_cache) if os.path.isfile((
            os.path.join(where_to_cache, file_))) and file_.startswith('__')
    ]
    if filename in cached_files:
        return True
    else:
        return False


def _cache_data(data, filename, shift):
    if shift:
        df = pd.DataFrame(data[1:])
    else:
        df = pd.DataFrame(data)
    df.to_csv(where_to_cache + filename, index=False, mode="a")


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
