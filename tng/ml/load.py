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

#where_to_cache = os.path.abspath('.') + '/tng/ml/__cached_history__/'
where_to_cache = os.path.dirname(os.path.abspath(__file__))+'/__cached_history__/'

def import_data(
    ticker, 
    timeframe, 
    start_date, 
    end_date, 
    reverse=True,
    split = (50, 25, 25),
    indicators = None
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

    check_home_folder()
    delete_old_files()
    start_date_str = start_date.strftime("%Y%m%d%H%M%S")
    end_date_str = end_date.strftime("%Y%m%d%H%M%S")
    filename = "__" + ticker + str(
        timeframe) + "_" + start_date_str + "_" + end_date_str + "__"
    if _is_cached(filename):
        read_data = pd.read_csv(where_to_cache + filename, index_col=None, header = None)
        data = separate_data(read_data, split)
    else:
        data = _load_data(ticker, timeframe, start_date, end_date, indicators)
        data = separate_data(data, split)
        if not reverse:
            data = data[::-1]
        _cache_data(data, filename)
    return data


def _load_data(ticker, timeframe, start_date, end_date, indicators):
    def on_bar(instrument):
        pass
        
    name = "import_data"
    regime = "SP"
    alg = TNG(name, regime, start_date, end_date)
    alg.addInstrument(ticker)
    alg.addTimeframe(ticker, timeframe)
    alg.run_backtest(on_bar)
    hist = list(alg.instruments)[0].rates[1:-50]
    del alg
    return hist


def separate_data(data, split):
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
        df.to_csv(where_to_cache+filename, index=False, mode = "a", header = False)

def check_home_folder():
    home_folder = os.path.dirname(os.path.abspath(__file__))
    if '__cached_history__' not in os.listdir(home_folder):
        os.mkdir(home_folder+'/__cached_history__/')

def delete_old_files():
    # where_to_cache = os.path.dirname(os.path.abspath(__file__))+'/__cached_history__/'
    #where_to_cache = os.path.abspath('.') + '/tng/ml/__cached_history__/'
    cached_files = [
        file_ for file_ in os.listdir(where_to_cache) if os.path.isfile((
            os.path.join(where_to_cache, file_))) and file_.startswith('__')
    ]
    for file_ in cached_files:
        timestamp = os.path.getmtime(where_to_cache+file_)
        this_moment = datetime.now()
        if (this_moment - datetime.fromtimestamp(timestamp)).days >= 30:
            os.remove(where_to_cache+file_)   
