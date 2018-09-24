import numpy as np
from tng.algorithm_backtest.limits import LOOKBACK_PERIOD as lookback
from tng.ind.ind import Indicators
from tng.data.data import dt


class Instrument(Indicators):
    """ Class contsins history data, candles and indicators.

        This class developed for storing history values available for
        user. Backtesting procedure will store 1 Instrument instance for 
        each pair of the form (ticker, timeframe), i.e. if user added
        one instrument and for this instrument added 3 timeframes then
        backtest procedure will contain 3 instances. If user added, say,
        two instruments (Beware! It may damage backtest!):
        ```python
        alg.addInstrument("btcusd")
        alg.addTimeframe("btcusd", 10, 15, 1440)
        alg.addInstrument("ltcbtc")
        alg.addTimeframe("ltcbtc", 15, 30, 240, 1440)
        ```
        then backtest procedure will store seven instances of Instrument class.

        Arguments:
            ticker (str): Name of the underlying asset.
            timeframe (int): Timeframe of the instrument.

        Attributes:
            ticker (str): Name of the underlying asset.
            timeframe (int): Timeframe of the instrument.
            time (int): Time of the beginning of the last fully formed candle.
            open (np.array): Numpy array of last LOOKBACK_PERIOD open prices
                of instrument.timeframe candles.
            high (np.array): Numpy array of last LOOKBACK_PERIOD high prices
                of instrument.timeframe candles.
            low (np.array): Numpy array of last LOOKBACK_PERIOD low prices
                of instrument.timeframe candles.
            close (np.array): Numpy array of last LOOKBACK_PERIOD close prices
                of instrument.timeframe candles.
            vol (np.array): Numpy array of last LOOKBACK_PERIOD volumes
                of instrument.timeframe candles.
            rates (np.array): Numpy array of dt type. Contains all
                instrument.timeframe candles that appears while backtest.
                instrument.rates[0] is a dt element.
                instrument.rates['open'] is a numpy array of all open price
                since the beginning of the backtest.
                Rates designed for recalculating technical indicators,
                so don't use this argument in your algorithm, it won't be
                available on the platform.
            candle_start_time (int): Time of the beginning of candle that is 
                not fully formed yet. This argument is not available ont the
                paltform.
            
    """

    def __init__(self, ticker, timeframe):
        Indicators.__init__(self, timeframe)
        self.ticker = ticker
        self.timeframe = timeframe
        self.now = 0
        self.time = np.zeros(lookback, dtype=np.int64)
        self.open = np.zeros(lookback)
        self.high = np.zeros(lookback)
        self.low = np.zeros(lookback)
        self.close = np.zeros(lookback)
        self.vol = np.zeros(lookback)
        self.rates = np.empty(lookback, dtype=dt)
        self.candles = None
        self.candle_ind = 0
        self.candle_start_time = None

    def __getitem__(self, indices):
        if isinstance(indices, int):
            if indices <= -lookback or indices >= lookback:
                err_str = "Index {} is out of range!".format(indices)
                raise IndexError(err_str)
            else:
                arr = np.array(
                    [(self.time[indices % lookback],
                      self.open[indices % lookback],
                      self.high[indices % lookback],
                      self.low[indices % lookback],
                      self.close[indices % lookback],
                      self.vol[indices % lookback])],
                    dtype=dt)
                arr = arr.view(np.recarray)
                return arr

        if isinstance(indices, slice):
            print(indices)
            print(type(indices))
            if indices.start <= -lookback or indices.stop >= lookback:
                err_str = "Index {} is out of range!".format(indices)
                raise IndexError(err_str)
            else:
                if indices.step is None:
                    size = indices.stop - indices.start
                    step = 1
                else:
                    size = (indices.stop - indices.start) // abs(
                        int(indices.step))
                    step = indices.step
                arr = np.empty_like((1, size), dtype=dt)
                for i in range(size):
                    arr[i] = np.array(
                        (self.time[indices.start + i * step],
                         self.open[indices.start + i * step],
                         self.high[indices.start + i * step],
                         self.low[indices.start + i * step],
                         self.close[indices.start + i * step],
                         self.vol[indices.start + i * step]),
                        dtype=dt)
                arr = arr.view(np.recarray)
                return arr
