from numpy import zeros
from tng.algorithm_backtest.limits import LOOKBACK_PERIOD as lookback
from tng.algorithm_backtest.ind import Indicators


class Instrument(Indicators):
    def __init__(self, ticker, timeframe, rates=None):
        Indicators.__init__(self, timeframe)
        self.ticker = ticker
        self.timeframe = timeframe
        self.time = 0
        self.open = zeros(lookback)
        self.high = zeros(lookback)
        self.low = zeros(lookback)
        self.close = zeros(lookback)
        self.vol = zeros(lookback)
        self.rates = None
        self.candle_start_time = None

    def __str__(self):
        s = ""
        for key, val in self.__dict__.items():
            if isinstance(val, list):
                s += (key + " = " + str(val) + "\n")
                pass
            else:
                s += ("\n" + key + " = " + str(val) + "\n")
        return s

    __repr__ = __str__
