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

where_to_cache = os.path.dirname(os.path.abspath(__file__))+'/__cached_history__/'


def import_data(
    ticker, 
    timeframe, 
    start_date, 
    end_date, 
    calculate_input,
    calculate_output,
    reverse=True,
    split = (50, 25, 25),
    indicators = None,
    cache = True
    ):
    if not isinstance(ticker, str) or \
        not isinstance(timeframe, int) or \
        not isinstance(start_date, datetime) or \
        not isinstance(end_date, datetime) or \
        not isinstance(split, tuple) \
        or len(split) > 3 or len(split) < 2:
        raise TypeError("Check types of arguments!")
    if sum(split) != 100:
        raise ValueError("Sum of values in split must be 100!")
    if not callable(calculate_input):
        raise TypeError("calculate_input must be callable!")
    if not callable(calculate_output):
        raise TypeError("calculate_output must be callable!")

    check_home_folder()
    delete_old_files()
    start_date_str = start_date.strftime("%Y%m%d%H%M%S")
    end_date_str = end_date.strftime("%Y%m%d%H%M%S")
    filename = "__" + ticker + str(
        timeframe) + "_" + start_date_str + "_" + end_date_str + "__"
    if _is_cached(filename):
        read_data = pd.read_csv(where_to_cache + filename)
        data = separate_data(read_data, split)
    else:
        data = _load_data(ticker, timeframe, start_date, end_date, indicators)
        data = separate_data(data, split)
        if not reverse:
            data = data[::-1]
        if cache:
            _cache_data(data, filename)
    return data


def _load_data(ticker, timeframe, start_date, end_date, indicators):
    data_columns = ['time', 'open', 'high', 'low', 'close', 'vol']
    sample = np.empty(len(data_columns))
    data = np.array([])
    ind_dict = dict()
    def on_bar(instrument):
        pass
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
                ind = eval("instrument."+str(key))
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
    alg.run_backtest(on_bar)
    del alg
    data = np.reshape(data, (len(data)//len(data_columns), len(data_columns)))
    data = pd.DataFrame(data, columns = data_columns)
    data = pd.concat([data, pd.DataFrame.from_dict(ind_dict)], axis = 1)
    return data


def separate_data(data, split):
    data = data.to_records()
    split_data = dict()
    if len(split) == 2:
        train_len = data.shape[0]*split[0]//100
        test_len = data.shape[0]*split[1]//100
        split_data['train'] = data[0:train_len]
        split_data['test'] = data[train_len:train_len+test_len]
    elif len(split) == 3:
        train_len = data.shape[0]*split[0]//100
        validation_len = data.shape[0]*split[1]//100
        test_len = data.shape[0]*split[2]//100
        split_data['train'] = data[0:train_len]
        split_data['validation'] = data[train_len:train_len+test_len]
        split_data['test'] = data[train_len+test_len:train_len+test_len+validation_len]
    return split_data


def _parse_indicator(ind_name, ind_value):
    if isinstance(ind_value, list):
        ret_dict = dict.fromkeys([ind_name])
        ret_dict[ind_name] = ind_value[1]
    else:
        keys = [ind_name+"."+str(elem) for elem in ind_value.__dict__.keys()]
        ret_dict = dict.fromkeys(keys)
        for key, value in (ind_value.__dict__.items()):
            ret_dict[ind_name+"."+key] = value[1]
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


def _cache_data(data, filename):
    for value in data.values():
        df = pd.DataFrame(value)
        df.to_csv(where_to_cache+filename, index=False, mode = "a")


def check_home_folder():
    home_folder = os.path.dirname(os.path.abspath(__file__))
    if '__cached_history__' not in os.listdir(home_folder):
        os.mkdir(home_folder+'/__cached_history__/')


def delete_old_files():
    cached_files = [
        file_ for file_ in os.listdir(where_to_cache) if os.path.isfile((
            os.path.join(where_to_cache, file_))) and file_.startswith('__')
    ]
    for file_ in cached_files:
        timestamp = os.path.getmtime(where_to_cache+file_)
        this_moment = datetime.now()
        if (this_moment - datetime.fromtimestamp(timestamp)).days > 31:
            os.remove(where_to_cache+file_)   