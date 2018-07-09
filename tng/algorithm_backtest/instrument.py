from numpy import zeros
from tng.algorithm_backtest.limits import LOOKBACK_PERIOD as lookback
from tng.ind.ind import Indicators


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