import sys
import os
from datetime import datetime
import time
import numpy as np
import pandas as pd
#sys.path.append('./../../')
from tng.algorithm_backtest.tng import TNG

dt = np.dtype({
    'names': ['time', 'open', 'high', 'low', 'close', 'vol'],
    'formats':
    ['uint64', 'float64', 'float64', 'float64', 'float64', 'float64']
})

where_to_cache = os.path.abspath('.')+'/tng/ml/__cached_history__/'

def import_data(ticker, 
                timeframe, 
                start_date, 
                end_date,
                reverse = True): 
    if not isinstance(ticker, str) or \
        not isinstance(timeframe, int) or \
        not isinstance(start_date, datetime) or \
        not isinstance(end_date, datetime):
        raise TypeError("Check types of arguments!")
    
    start_date_str = start_date.strftime("%Y%m%d%H%M%S")
    end_date_str = end_date.strftime("%Y%m%d%H%M%S")
    filename = "__"+ticker+str(timeframe)+"_"+start_date_str+"_"+end_date_str+"__"
    if _is_cached(filename):
        data = pd.read_csv(where_to_cache+filename, index_col=None, dtype=dt)
        data = data.to_records(index=False)
    else:
        data = _load_data_from_pack(ticker, timeframe, start_date, end_date)
        if not reverse:
            data = data[::-1]
        _cache_data(data, filename)
    return data

def _load_data_from_pack(ticker, timeframe, start_date, end_date):
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

def _is_cached(filename):    
    where_to_cache = os.path.abspath('.')+'/tng/ml/__cached_history__/'
    cached_files = [
        file_ for file_ in os.listdir(where_to_cache) if 
        os.path.isfile((os.path.join(where_to_cache, file_))) and
        file_.startswith('__')
    ]
    if filename in cached_files:
        return True
    else:
        return False

def _cache_data(data, filename):
    where_to_cache = os.path.abspath('.')+'/tng/ml/__cached_history__/'+filename
    df = pd.DataFrame(data)
    df.to_csv(where_to_cache, index = False)
