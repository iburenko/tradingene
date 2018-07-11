from numpy import zeros
from tng.algorithm_backtest.limits import LOOKBACK_PERIOD as lookback
from tng.ind.ind import Indicators


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

        # Arguments:
            ticker (str): Name of the underlying asset.
            timeframe (int): Timeframe of the instrument.

        # Attributes:
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
        self.ind = Indicators(timeframe)
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
