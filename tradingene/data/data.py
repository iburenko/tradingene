import os, sys
import platform
import time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import requests
import json
from tradingene.algorithm_backtest.limits import instrument_ids
import tradingene.algorithm_backtest.limits as limits
from tradingene.data.date_init import moex_start_date, moex_end_date
from tradingene.algorithm_backtest.limits import moex_tickers

dt = np.dtype({
    'names': ['time', 'open', 'high', 'low', 'close', 'vol'],
    'formats':
    ['uint64', 'float64', 'float64', 'float64', 'float64', 'float64']
})
""" np.dtype: Numpy dtype of signle minute candle stored from history data.

    Single element of history consists of the following fields:
        time (int64): Open time of a minute candle.
        open (float64): Open price of a minute candle.
        high (float64): The highest price of a minute candle.
        low (float64): The lowest price of a minute candle.
        close (float64): Close price of a minute candle.
        vol (float64): Volume of a minute candle.
"""


class Data:
    """ Class for loading instrument history. """

    if platform.system() != "Windows":
        hist_path = os.path.dirname(
            os.path.abspath(__file__)) + "/__cached_history__/"
    else:
        hist_path = os.path.dirname(
            os.path.abspath(__file__)) + "\\__cached_history__\\"
    

    def __init__(self):
        pass

    @classmethod
    def load_data(cls, filename, start_date, end_date, pre=0):
        """ Loads file from the drive and returns history data. 
        
            Arguments:
                filename (str): Name of the asset. Its history will
                    be loaded from .csv file.
                start_date (datetime.datetime): From this timestamp data
                    will be loaded.
                end_date (datetime.datetime): Till this timestamp data
                    will be loaded.

            Returns:
                hist_data(np.record): Numpy array of minute candles.
        """

        def find_start_end(all_data, start_date, end_date):

            while True:
                start = all_data[all_data['time'] == start_date].index.values
                if len(start):
                    start = int(start)
                    break
                else:
                    #works only if the first candle is in start day -- correct
                    start_date += 100
            while True:
                end = all_data[all_data['time'] == (end_date)].index.values
                if len(end):
                    if not pre:
                        end = int(end) + 1
                    else:
                        end = int(end)
                    break
                else:
                    end_date += 100
            return start, end

        earliest_start = limits.EARLISET_START
        if start_date < earliest_start:
            warn_str = "Can't get data from {}. Data are available form 01.01.2017".format(
                start_date)
            start_date = earliest_start
        if end_date > datetime.today():
            warn_str = "Can't get data till {}. Data are available till today ({})".format(
                end_date, datetime.today())
            _date = datetime.today()
            end_date = datetime(_date.year, _date.month, _date.day)
        if not cls._check_file(filename):
            data = cls._download_minute_data(start_date, end_date, filename)
            if len(data) == 0:
                raise Exception("Data was not downloaded! Probably there are no data for this period!")
            data.to_csv(Data.hist_path + filename + ".csv", index=False)
        else:
            new_dates = cls._find_uncached_dates(start_date, end_date,
                                                 filename)
            
            for dates in new_dates:
                data = cls._download_minute_data(dates[0], dates[1], filename)
                flag = dates[2]
                if flag == 1:
                    # append to the begging
                    cached_data = pd.read_csv(Data.hist_path + filename +
                                              ".csv")
                    data = pd.concat([data, cached_data], ignore_index=True)
                    data.to_csv(
                        Data.hist_path + filename + ".csv", index=False)
                elif flag == 2:
                    # appeng to the end
                    cached_data = pd.read_csv(Data.hist_path + filename +
                                              ".csv")
                    data = pd.concat([cached_data, data], ignore_index=True)
                    data.to_csv(
                        Data.hist_path + filename + ".csv", index=False)
            if not new_dates:
                data = pd.read_csv(Data.hist_path + filename + ".csv")
            start_date_int = int(start_date.strftime("%Y%m%d%H%M%S"))
            if pre:
                end_date -= timedelta(minutes=1)
            end_date_int = int(end_date.strftime("%Y%m%d%H%M%S"))
            data = data[data['time'].between(
                start_date_int, end_date_int, inclusive=True)]
        return data[::-1]

    @classmethod
    def _download_minute_data(cls, start_date, end_date, filename):
        end_date -= timedelta(minutes=1)
        if filename in instrument_ids.keys():
            instr_id = instrument_ids[filename]
        else:
            raise ValueError("Instrument {} was not found!".format(filename))
        iters = (end_date - start_date).days//90
        data = pd.DataFrame()            
        for i in range(iters):
            if i != 0:
                iter_start_date = start_date + timedelta(days=90*i) + timedelta(minutes=1)
            else:
                iter_start_date = start_date
            iter_end_date = start_date + timedelta(days=90*(i+1))
            new_data = cls._download_data(iter_start_date, iter_end_date, instr_id)
            data = data.append(new_data, ignore_index=True)
        if iters == 0:
            new_data = cls._download_data(start_date, end_date, instr_id)
        else:
            iter_end_date += timedelta(minutes=1)
            new_data = cls._download_data(iter_end_date, end_date, instr_id)
        data = data.append(new_data, ignore_index=True)
        return data

    @staticmethod
    def _check_file(filename):
        saved = [
            file_ for file_ in os.listdir(Data.hist_path)
            if file_.startswith(filename)
        ]
        if not saved:
            return False
        else:
            return True

    @classmethod
    def _find_uncached_dates(cls, start_date, end_date, filename):
        to_cache = list()
        saved = [
            file_ for file_ in os.listdir(Data.hist_path)
            if file_.startswith(filename)
        ][0]
        df = pd.read_csv(Data.hist_path + saved)
        if filename.startswith("__"):    
            cached_start_time = str(df['time'].iloc[-1])
            cached_end_time = str(df['time'].iloc[0])    
        else:
            cached_start_time = str(df['time'].iloc[0])
            cached_end_time = str(df['time'].iloc[-1])
        prev_start_date = \
                datetime(*(time.strptime(cached_start_time, "%Y%m%d%H%M%S")[0:6]))
        prev_end_date = \
                datetime(*(time.strptime(cached_end_time, "%Y%m%d%H%M%S")[0:6]))
        prev_end_date += timedelta(minutes=1)
        if start_date < prev_start_date:
            to_cache.append((start_date, prev_start_date, 1))
        if end_date > prev_end_date:
            to_cache.append((prev_end_date, end_date, 2))
        return to_cache

    @staticmethod
    def _download_data(iter_start_date, iter_end_date, instr_id):
        t = time.time()
        iter_start_date = int(iter_start_date.strftime("%Y%m%d%H%M%S"))
        iter_end_date = int(iter_end_date.strftime("%Y%m%d%H%M%S"))
        req_start_date = iter_start_date * 1000
        req_end_date = iter_end_date * 1000
        url = "https://candles.tradingene.com/candles?instrument_id=" + \
            str(instr_id)+"&from="+str(req_start_date)+"&to="+str(req_end_date)
        data = requests.get(url)
        if not data:
            raise Exception("Data was not downloaded! Please try again!")
        obj = data.json()
        df_data = pd.DataFrame(
            obj, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        df_data.drop_duplicates(subset=['time'], inplace=True)
        df_data['time'] = df_data['time'].astype('int64')
        df_data['time'] //= 1000
        df_data.rename(columns={'volume': 'vol'}, inplace=True)
        return df_data
