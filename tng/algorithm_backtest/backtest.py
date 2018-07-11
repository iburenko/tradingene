from warnings import warn
import time
import numpy as np
from datetime import datetime, timedelta
from tng.algorithm_backtest.environment import Environment
from tng.algorithm_backtest.position import Position
from tng.algorithm_backtest.time_event import TimeEvent
from tng.algorithm_backtest.price_event import PriceEvent
import tng.algorithm_backtest.limits as limits
from tng.algorithm_backtest.data import Data, dt
from tng.ind.spread_estimation_corwin_schultz import corwin_schultz


class Backtest(Environment):
    """ Runs the backtest.

        Constructor of this class will automatically 
        invoke by the inherited class TradeActivity.

        # Arguments:
            args (tuple): Tuple of variables that needed for initialization
                of the super class Algorithm.

        # Attributes:
            history_data (dict): Contains loaded history data 
                of the specified instrument.
            completed_timeframes (list): List of timeframes that was completed
                while run of backtest.
            completed_tickers (list): List of tickers that have at least one
                completed timeframe and appears in the last minute candle that
                was send to backtest.
            now (int): Time of the beggining of the most recent minute candle.
            recent_price (float): The most recent price of an instrument.
                Minute candle divides into four ticks:
                a) if a candle goes down: open, high, low, close;
                b) otherwise: open, low, high, close.
            spread (float): Spread. Specified for each instrument.
            instruments (set): Set of intances of Instrument class.
                each instance contains information about opens, highs,
                lows, closes, volumes, values of indicators. 
            time_events (list): List of instances of TimeEvents class.
                Time events added by user in the onBar function.
            price_events (list): List of instances of PriceEvent class.
                Price events added by user in the onBar function.
    """

    def __init__(self, *args):
        name, regime = args[0], args[1]
        start_date, end_date = args[2], args[3]
        super(Backtest, self).__init__(name, regime, start_date, end_date)
        self.history_data = dict()
        self.completed_timeframes = list()
        self.completed_tickers = list()
        self._now = 0
        self._recent_price = 0
        self.spread = 0
        self.instruments = set()
        self.time_events = list()
        self.price_events = list()

################################################################################

    def run_backtest(self, on_bar_function):
        """ Runs backtest of an algorithm. 
        
        Args:
            on_bar_function (function): user-define function
                that is called after each fully formed candle.

        Returns:
            None.
        
        Raises:
            TypeError: if on_bar_function is not callable.
        
        """
        if not callable(on_bar_function):
            err_str = "on_bar_function must be callable, not of "+\
                      "{} type!".format(type(on_bar_function).__name__)
            raise TypeError(err_str)
        self._load_data(self.start_date, self.end_date)
        self._set_spread()
        candle_generator = self._iterate_data(self.start_date, self.end_date,
                                              self.history_data)
        self._run_generator(candle_generator, on_bar_function)

    def _run_generator(self, generator, on_bar_function):
        candles = next(generator)
        minutes_left = 1
        self._update_instruments(candles)
        try:
            complete_timeframes = list()
            complete_tickers = list()
            instrs = set()
            while True:
                candles = next(generator)
                self._update_recent_price(candles)
                time_frames = self._list_all_timeframes()
                complete_timeframes = \
                        self._completed_timeframes(minutes_left, time_frames)
                complete_tickers = self._completed_tickers(
                    complete_timeframes, complete_tickers)
                on_bar_tickers = {ticker \
                        for ticker in complete_tickers if ticker in candles}
                instrs |= self._completed_instruments(complete_tickers,
                                                      complete_timeframes)
                call = {
                    instrument
                    for instrument in instrs
                    if instrument.ticker in on_bar_tickers
                }
                for instr in call:
                    instr = self._reload_instrument(instr, candles)
                instrs -= call
                complete_tickers = list(set(complete_tickers) - on_bar_tickers)
                list(map(on_bar_function, call))
                minutes_left += 1
                self._update_instruments(candles)
                self._minute_to_ticks(candles)
        except StopIteration:
            self._update_last_candle()

    def _update_recent_price(self, candles):
        ticker = list(self.ticker_timeframes)[0]
        if ticker in candles.keys():
            candle = np.array(([candles[ticker]]), dtype=dt)
            self.recent_price = candle['open']

    def _minute_to_ticks(self, candles):
        ticker = list(self.ticker_timeframes)[0]
        if ticker in candles.keys():
            candle = np.array(([candles[ticker]]), dtype=dt)
            self.recent_price = candle['open']
            if candle['open'] < candle['close']:
                self.recent_price = candle['low']
            else:
                self.recent_price = candle['high']
            if candle['open'] < candle['close']:
                self.recent_price = candle['high']
            else:
                self.recent_price = candle['low']
            self.recent_price = candle['close']

    def _iterate_data(self, start_date, end_date, history_data):
        current_time = start_date
        backtest_time = int(current_time.strftime("%Y%m%d%H%M%S"))
        time_ticks = dict.fromkeys(self.ticker_timeframes, -1)
        while current_time <= end_date:
            self.now = backtest_time
            ans = dict()
            for ticker in self.ticker_timeframes:
                ind = time_ticks[ticker]
                try:
                    ticker_time = history_data[ticker][ind]['time']
                except:
                    continue
                if ticker_time == backtest_time:
                    time_ticks[ticker] -= 1
                    ans[ticker] = history_data[ticker][ind]
                else:
                    pass
            current_time = current_time + timedelta(minutes=1)
            backtest_time = int(current_time.strftime("%Y%m%d%H%M%S"))
            yield ans

    def _update_instruments(self, candles):
        for instrument in self.instruments:
            ticker = instrument.ticker
            if ticker in candles:
                candle = candles[ticker]
            else:
                continue
            if instrument.open[0] == 0:
                instrument.open[0] = candle.open
            instrument.high[0] = max(instrument.high[0], candle['high'])
            if instrument.low[0] == 0:
                instrument.low[0] = candle['low']
            else:
                instrument.low[0] = min(instrument.low[0], candle['low'])
            instrument.close[0] = candle['close']
            instrument.vol[0] += candle['vol']

    def _reload_instrument(self, instrument, candles):
        def correct_candle_time(time_, timeframe):
            minutes_ = ((time_ // 100) % 100)
            hours_ = ((time_ // 10000) % 100)
            days_ = ((time_ // 1000000) % 100)
            total_minutes = (days_ - 1) * 1440 + hours_ * 60 + minutes_
            total_minutes %= timeframe
            minutes_ = (time_) % timeframe
            time_ = datetime(*(time.strptime(str(time_), \
                                            "%Y%m%d%H%M%S")[0:6]))
            time_ -= timedelta(minutes=total_minutes)
            time_ = int(time_.strftime("%Y%m%d%H%M%S"))
            return time_

        self._set_spread()

        candle = candles[instrument.ticker]
        for instr in self.instruments:
            if instr.ticker == instrument.ticker and \
               instr.timeframe == instrument.timeframe:
                time_ = datetime(*(time.strptime(str(self.now), \
                                           "%Y%m%d%H%M%S")[0:6]))
                open_price = np.array([candle['open']])
                new_time = int(time_.strftime("%Y%m%d%H%M%S"))
                last_time = time_ - timedelta(minutes=instr.timeframe)
                instr.time = int(last_time.strftime("%Y%m%d%H%M%S"))
                instr.open = np.concatenate((open_price, instr.open[:-1]))
                instr.high = np.concatenate((open_price, instr.high[:-1]))
                instr.low = np.concatenate((open_price, instr.low[:-1]))
                instr.close = np.concatenate((open_price, instr.close[:-1]))
                instr.vol = np.concatenate(([0], instr.vol[:-1]))
                last_time = correct_candle_time(instr.candle_start_time,
                                                instr.timeframe)
                new_time = correct_candle_time(new_time, instr.timeframe)
                last_candle = np.array([(last_time, instr.open[1], \
                                        instr.high[1], instr.low[1], \
                                        instr.close[1], instr.vol[1])], \
                                        dtype = dt)

                new_candle = np.array([(new_time, instr.open[0], instr.high[0],\
                                        instr.low[0], instr.close[0], \
                                        instr.vol[0])], dtype = dt)
                if instr.rates is None:
                    if last_candle['open'] == 0:
                        instr.rates = new_candle
                    else:
                        instr.rates = last_candle
                        instr.rates = np.concatenate((new_candle, instr.rates))
                else:
                    instr.rates[0] = last_candle
                    instr.rates = np.concatenate((new_candle, instr.rates))
                instr.candle_start_time = self.now
        return instrument

    def _update_last_candle(self):
        for instr in self.instruments:
            open_price = np.array([0.])
            time_ = datetime(*(time.strptime(str(self.now), \
                                        "%Y%m%d%H%M%S")[0:6]))
            new_time = int(time_.strftime("%Y%m%d%H%M%S"))
            last_time = time_ - timedelta(minutes=instr.timeframe)
            instr.time = int(last_time.strftime("%Y%m%d%H%M%S"))
            instr.open = np.concatenate((open_price, instr.open[:-1]))
            instr.high = np.concatenate((open_price, instr.high[:-1]))
            instr.low = np.concatenate((open_price, instr.low[:-1]))
            instr.close = np.concatenate((open_price, instr.close[:-1]))
            instr.vol = np.concatenate(([0], instr.vol[:-1]))
            last_candle = np.array([(instr.time, instr.open[1], \
                                    instr.high[1], instr.low[1], \
                                    instr.close[1], instr.vol[1])], \
                                    dtype = dt)
            new_candle = np.array([(new_time, instr.open[0], \
                                    instr.high[0], instr.low[0],\
                                    instr.close[0], instr.vol[0])],\
                                    dtype = dt)
            instr.rates[0] = last_candle
            instr.rates = np.concatenate((new_candle, instr.rates))

    def _completed_instruments(self, tickers, timeframes):
        instr = set()
        for instrument in self.instruments:
            ticker = instrument.ticker
            timeframe = instrument.timeframe
            if ticker in tickers and timeframe in timeframes:
                instr |= {instrument}
        return instr

    def _list_all_timeframes(self):
        time_frames = set()
        for value in self.ticker_timeframes.values():
            time_frames |= set(value)
        return sorted(list(time_frames))

    def _completed_timeframes(self, minutes_left, timeframes):
        completed_tfs = [timeframe\
                for timeframe in timeframes if minutes_left % timeframe == 0]
        return sorted(completed_tfs)

    def _completed_tickers(self, completed_timeframes, ct):
        new_set = {ticker for ticker, timeframes \
                          in self.ticker_timeframes.items()\
                          if set(completed_timeframes) & set(timeframes)}
        return list(new_set | set(ct))

    def _load_data(self, start_date, end_date):
        for ticker in self.ticker_timeframes.keys():
            self._load_pre_data()
            ticker_data = Data.load_data(ticker, start_date, end_date)
            self.history_data[ticker] = ticker_data
            ticker_instrs = [
                instr for instr in self.instruments if instr.ticker == ticker
            ]
            for instr in ticker_instrs:
                instr.candle_start_time = int(
                    start_date.strftime("%Y%m%d%H%M%S"))

    def _foo(self, instrument):
        pass

    def _load_pre_data(self):
        lookback = limits.LOOKBACK_PERIOD
        earliest_start = eval(limits.EARLISET_START)
        pre_data = dict.fromkeys(self.ticker_timeframes)
        pre_end_date = self.start_date
        pre_start_array = list()
        for ticker in self.ticker_timeframes.keys():
            timeframe = max(self.ticker_timeframes[ticker])
            pre_start_date = \
                    self.start_date -  timedelta(minutes = lookback * timeframe)
            if pre_start_date < earliest_start:
                warn("Some values in history will be zero! Data available from"+\
                     " 01.01.2017")
                pre_start_date = self.start_date
            pre_start_array.append(pre_start_date)
        pre_start_date = min(pre_start_array)
        for ticker in self.ticker_timeframes.keys():
            ticker_data = Data.load_data(ticker, pre_start_date, pre_end_date)
            pre_data[ticker] = ticker_data
            ticker_instrs = [
                instr for instr in self.instruments if instr.ticker == ticker
            ]
            for instr in ticker_instrs:
                instr.candle_start_time = int(
                    pre_start_date.strftime("%Y%m%d%H%M%S"))
        pre_data_candles_generator = self._iterate_data(
            pre_start_date, pre_end_date, pre_data)
        self._run_generator(pre_data_candles_generator, self._foo)

    def _set_spread(self):
        ticker = list(self.ticker_timeframes)[0]
        if ticker == "btcusd":
            self.spread = limits.BTCUSD_SPREAD
        elif ticker == "ethusd":
            self.spread = limits.ETHUSD_SPREAD
        elif ticker == "ltcusd":
            self.spread = limits.LTCUSD_SPREAD
        elif ticker == "ethbtc":
            self.spread = limits.ETHBTC_SPREAD
        elif ticker == "ltcbtc":
            self.spread = limits.LTCBTC_SPREAD
        elif ticker == "dshbtc":
            self.spread = limits.DSHBTC_SPREAD
        elif ticker == "xrpbtc":
            self.spread = limits.XRPBTC_SPREAD
        else:
            raise NameError("Spread cannot be set, unknown ticker!")


################################################################################

    @property
    def now(self):
        return self._now

    @now.setter
    def now(self, value):
        self._now = value
        TimeEvent.check(self)

    @now.deleter
    def now(self):
        self._now = None

    @property
    def recent_price(self):
        return self._recent_price

    @recent_price.setter
    def recent_price(self, value):
        self._recent_price = value
        Position.check_sltp(self)
        PriceEvent.check(self)

    @recent_price.deleter
    def recent_price(self):
        self._recent_price = None
