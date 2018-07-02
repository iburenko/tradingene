from datetime import datetime
from numpy.random import randint
from warnings import warn
from tng.algorithm_backtest.backtest import Backtest
from tng.algorithm_backtest.position import Position
from tng.algorithm_backtest.trade import Trade
from tng.algorithm_backtest.price_event import PriceEvent
from tng.algorithm_backtest.time_event import TimeEvent
from tng.algorithm_backtest.limits import MAX_AVAILABLE_VOLUME


class TradeActivity(Backtest):
    """
    Working with positions. This version works if algorithms
    uses only one instrument.
    """

    def __init__(self, *args):
        name, regime = args[0], args[1]
        start_date, end_date = args[2], args[3]
        super(TradeActivity, self).__init__(name, regime, start_date, end_date)
        self.positions = list()

    def openPosition(self, ticker=None):
        """Open position without acquiring any asset

        # Arguments:
            ticker (str): Asset for which position will open.
                    If an algorithm uses only one asset you can
                    not to specify explicitly ticker, but if an
                    algorithm uses several instruments ticker
                    must be specified
        """
        new_pos = None
        is_closed = self._is_last_pos_closed()
        pos_ticker = list(self.ticker_timeframes)[0]
        if is_closed == None:
            pos_id = randint(2**1, 2**32 - 1)
            new_pos = Position(pos_id, pos_ticker, self.now)
        elif is_closed:
            pos_id = is_closed + 1
            new_pos = Position(pos_id, pos_ticker, self.now)
        else:
            warn(
                "Can't open new position because last position is not closed!")
        if new_pos:
            self.positions.append(new_pos)
            return new_pos.id
        else:
            return None

    def buy(self, volume=1):
        """
        Opens position if position was closed and buys volume lots.
        If volume of already bought lots +  current volume exceeds given
        volume limit, buy as much as posiible.
        """
        if volume <= 0:
            warn("Volume must be positive! Nothing will happen!")
            return None
        elif volume > MAX_AVAILABLE_VOLUME:
            raise ValueError("Can't buy! Volume exceeds upper limit!")
        if self.regime == "SP":
            volume = 1
            is_closed = self._is_last_pos_closed()
            if not is_closed:
                if is_closed == None:
                    self.openPosition()
                if self.positions[-1].trades:
                    if self.positions[-1].trades[-1].side == 1:
                        warn("Can't buy since there is an open buy!")
                    else:
                        self.closePosition()
                        self.openPosition()
                        trade_id = self._open_trade(volume, side=1)
                else:
                    trade_id = self._open_trade(volume, side=1)
            else:
                self.openPosition()
                trade_id = self._open_trade(volume, side=1)
        else:
            is_closed = self._is_last_pos_closed()
            if is_closed == None or is_closed > 0:
                self.openPosition()
                trade_id = self._open_trade(volume, side=1)
            else:
                volume_used = self.positions[-1].volume_used
                if abs(volume_used + volume) > MAX_AVAILABLE_VOLUME:
                    s = "You use {} number of lots.".format(volume_used)+\
                        "Can't buy {} lots, since total volume".format(volume)+\
                        "will exceed the upper limit!"
                    raise ValueError(s)
                else:
                    trade_id = self._open_trade(volume, side=1)

    def sell(self, volume=1):
        if volume <= 0:
            warn("Volume must be positive! Nothing will happen!")
            return None
        elif volume > MAX_AVAILABLE_VOLUME:
            raise ValueError("Can't buy! Volume exceeds upper limit!")
        if self.regime == "SP":
            volume = -1
            is_closed = self._is_last_pos_closed()
            if not is_closed:
                if is_closed == None:
                    self.openPosition()
                if self.positions[-1].trades:
                    if self.positions[-1].trades[-1].side == -1:
                        warn("Can't sell since there is an open sell!")
                    else:
                        self.closePosition()
                        self.openPosition()
                        trade_id = self._open_trade(volume, side=-1)
                else:
                    trade_id = self._open_trade(volume, side=-1)
            else:
                self.openPosition()
                trade_id = self._open_trade(volume, side=-1)
        else:
            volume *= -1
            is_closed = self._is_last_pos_closed()
            if is_closed == None or is_closed > 0:
                self.openPosition()
                trade_id = self._open_trade(volume, side=-1)
            else:
                volume_used = self.positions[-1].volume_used
                if abs(volume_used + volume) > MAX_AVAILABLE_VOLUME:
                    s = "You use {} number of lots.".format(volume_used)+\
                        "Can't sell {} lots, since total volume".format(volume)+\
                        "will exceed the upper limit!"
                    raise ValueError(s)
                else:
                    trade_id = self._open_trade(volume, side=-1)

    def openLong(self, volume=1):
        is_closed = self._is_last_pos_closed()
        if is_closed is not None and not is_closed:
            warn("Can't open long since there is an open position")
            pos_id = None
        else:
            pos_id = self.openPosition()
            self.buy(volume)
        return pos_id

    def openShort(self, volume=1):
        is_closed = self._is_last_pos_closed()
        if is_closed is not None and not is_closed:
            warn("Can't open short since there is an open position")
            pos_id = None
        else:
            pos_id = self.openPosition()
            self.sell(volume)
        return pos_id

    def setSL(self, loss=None):
        is_closed = self._is_last_pos_closed()
        if not is_closed:
            if loss > 0:
                self.positions[-1].stop_loss = loss
            elif loss == 0:
                self.positions[-1].stop_loss = None
            else:
                raise ValueError("Cannot set stoploss! Stoploss can't be None")

    def setTP(self, profit=None):
        is_closed = self._is_last_pos_closed()
        if not is_closed:
            if profit > 0:
                self.positions[-1].take_profit = profit
            elif profit == 0:
                self.positions[-1].take_profit = None
            else:
                raise ValueError("Cannot set stoploss! Stoploss can't be None")

    def setSLTP(self, loss, profit):
        self.set_sl(loss)
        self.set_tp(profit)

    def closePosition(self, id=None):
        """
        Closes last opened position if id == None,
        otherwise closes position with specified id
        """
        closed = False
        if id == None:
            is_closed = self._is_last_pos_closed()
            if is_closed is not None and not is_closed:
                last_pos = self.positions[-1]
                last_pos.close_time = self.now
                last_pos.closed = True
                closed = True
                if last_pos.on_close is not None:
                    last_pos.on_close()
            else:
                warn("Can't close position! There is no opened position!")
        else:
            for pos in self.positions:
                if pos.id == id:
                    if pos.closed:
                        warn("Can't close position with id {}".format(id)+\
                             " because it is closed already!")
                    else:
                        pos.close_time = self.now
                        pos.closed = True
                        closed = True
                        if pos.on_close is not None:
                            pos.on_close()
                    break
                else:
                    continue
        if closed:
            volume_traded = 0
            for trade in self.positions[-1].trades:
                volume_traded += abs(trade.volume)
            self.positions[-1].profit -= (2 * volume_traded * self.spread)

    def onPositionClose(self, pos_id, handler):
        pos = [pos for pos in self.positions if pos.id == pos_id]
        if len(pos):
            pos = pos[0]
        else:
            raise ValueError("Position with specified ID was not found!")
        if callable(handler):
            pos.on_close = handler
        else:
            raise TypeError("Can't call on_position_close!"+\
                            "{} is not callable!".format(handler))
        return None

    def getAvailableVolume(self):
        is_closed = self._is_last_pos_closed()
        if is_closed == False:
            return self.positions[-1].available_volume()
        else:
            warn(
                "Can't get available volume since there is no opened position!"
            )
            return None

    def getLastPrice(self, ticker=None):
        try:
            if not ticker:
                assert len(self.ticker_timeframes) == 1
                return list(self.instruments)[0].close[0]
            else:
                found = False
                for instrument in self.instruments:
                    if instrument.ticker == ticker:
                        return instrument.close[0]
                if not found:
                    raise NameError("Ticker {} was not found!".format(ticker))
        except AssertionError:
            raise NameError("Ticker {} was not specified!".format(ticker))

    def on(self, type_=None, params=None, handler=None):
        ticker = list(self.ticker_timeframes)[0]
        if type_ == "Price":
            if self._check_price_params(params, handler):
                if self.recent_price <= params:
                    trigger = 1
                elif self.recent_price > params:
                    trigger = -1
                new_price_event = PriceEvent(ticker, params, trigger, handler)
                new_price_event.id = randint(2**1, 2**32 - 1)
                self.price_events.append(new_price_event)
                return new_price_event.id
        elif type_ == "Time":
            time = self._check_time_params(params, handler)
            if time is not None:
                new_time_event = TimeEvent(ticker, time, handler)
                new_time_event.id = randint(2**1, 2**32 - 1)
                self.time_events.append(new_time_event)
                return new_time_event.id
        else:
            raise ValueError("Unknown type of an event {}!".format(type_))

    def off(self, id):
        for price_event in self.price_events:
            if price_event.id == id:
                self.price_events.remove(price_event)
                return
        for time_event in self.time_events:
            if time_event.id == id:
                self.time_events.remove(time_event)
                return
        warn("Event with id {} was not found!".format(id))

    def _check_price_params(self, params, handler):
        if isinstance(params, int) or isinstance(params, float):
            if callable(handler):
                for event in self.price_events:
                    if event.threshold == params and event.handler == handler:
                        warn("This Price event already exists!")
                        return None
                return True
            else:
                raise TypeError("Value in handler is not callable!")
        else:
            raise TypeError("Price must be of Numeric type")

    def _check_time_params(self, params, handler):
        if isinstance(params, datetime):
            if callable(handler):
                time = int(datetime.strftime(params, "%Y%m%d%H%M%S"))
                if time <= self.now:
                    warn(
                        "Can't add new time event! Specified time is in past!")
                    return None
                for event in self.time_events:
                    if event.time == time and event.handler == handler:
                        warn("This Time event already exists!")
                        return None
                return time
            else:
                raise TypeError("Value in handler is not callable!")
        else:
            raise TypeError("Time must be of datetime type")

    def _is_last_pos_closed(self):
        """
        Returns last position id if last position is closed;
        Returns False if last position is open;
        Returns None if there is no last position
        """

        if self.positions:
            if self.positions[-1].closed:
                return self.positions[-1].id
            else:
                return False
        else:
            return None

    def _open_trade(self, volume, side):
        if self.positions[-1].trades:
            trade_id = self.positions[-1].trades[-1].id + 1
        else:
            trade_id = randint(2**1, 2**32 - 1)
        open_price = self.recent_price
        new_trade = Trade(trade_id, open_price, volume, self.now)
        self.positions[-1].trades.append(new_trade)
        self.positions[-1].volume_used += volume
        return trade_id
