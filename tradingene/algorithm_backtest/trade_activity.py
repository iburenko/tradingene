from datetime import datetime
from numpy import sign
from numpy.random import randint
from warnings import warn
from tradingene.algorithm_backtest.backtest import Backtest
from tradingene.algorithm_backtest.position import Position
from tradingene.algorithm_backtest.trade import Trade
from tradingene.algorithm_backtest.price_event import PriceEvent
from tradingene.algorithm_backtest.time_event import TimeEvent
from tradingene.algorithm_backtest.limits import MAX_AVAILABLE_VOLUME


class TradeActivity(Backtest):
    """Class contains methods needed for mimicking trading activity.

        Constructor of this class will invoke by the inherited 
        class TNG.

        Arguments:
            args (tuple): Tuple of variables that needed for initialization
                of the super class Backtest.

        Attributes:
            positions (list): List of all positions. Each position is
                an instance of Position class.
    """

    def __init__(self, *args):
        name, regime = args[0], args[1]
        start_date, end_date = args[2], args[3]
        super(TradeActivity, self).__init__(name, regime, start_date, end_date)
        self.positions = list()


    def openPosition(self, ticker=None):
        """ Open position without acquiring any asset.

            Arguments:
                ticker (str): Asset for which position will open.
                        At the moment algorithm is not able to use
                        several instruments. Only the first added
                        instrument will be used despite of ticker
                        received by the function.

            Warns:
                warn: If you are trying to open a new position
                    but the last is not closed. Only one opened
                    position is allowed.

            Returns:
                int: Random int if the first position is opened.
                    Increased by one last position's id if there
                    was opened position.
                None: If position wasn't opened.

            Example:
            ```python
                # This example opens a position for btcusd.
                alg = TNG(ticker, timeframe, start_date, end_date)
                alg.addInstrument("btcusd")
                alg.addTimeframe("btcusd", 10)
                alg.openPosition()
            ```
            ```python
                # This example opens a position for btcusd.
                alg = TNG(ticker, timeframe, start_date, end_date)
                alg.addInstrument("btcusd")
                alg.addTimeframe("btcusd", 10)
                alg.openPosition("btcusd")
            ```
            ```python
                # This example opens a position for btcusd.
                alg = TNG(ticker, timeframe, start_date, end_date)
                alg.addInstrument("btcusd")
                alg.addTimeframe("btcusd", 10)
                alg.openPosition("ethbtc")
            ```
            ```python
                # This example opens a position for btcusd.
                alg = TNG(ticker, timeframe, start_date, end_date)
                alg.addInstrument("btcusd")
                alg.addInstrument("ethbtc")
                alg.addTimeframe("btcusd", 10)
                alg.addTimeframe("ethbtc", 30)
                alg.openPosition("ethbtc")
            ```
            ```python
                # This example opens a position for ethbtc.
                alg = TNG(ticker, timeframe, start_date, end_date)
                alg.addInstrument("ethbtc")
                alg.addInstrument("btcusd")
                alg.addTimeframe("btcusd", 10)
                alg.addTimeframe("ethbtc", 30)
                alg.openPosition("ethbtc")
            ```
        """

        new_pos = None
        is_closed = self._is_last_pos_closed()
        pos_ticker = list(self.ticker_timeframes)[0]
        if is_closed == None:
            pos_id = randint(2**1, 2**31 - 1)
            new_pos = Position(pos_id, pos_ticker, self.now)
        elif is_closed:
            pos_id = is_closed + 1
            new_pos = Position(pos_id, pos_ticker, self.now)
        else:
            warn(
                "Can't open new position because last position is not closed!\n"
            )
        if new_pos:
            self.positions.append(new_pos)
            return new_pos.id
        else:
            return None


    def buy(self, volume=1):
        """ Buys specified volume of an asset.

            In Single Position regime:
            buys 1 lot despite of volume received 
            by the function. If the last position
            was closed new position will open automatically.
            If the last position is open and short then this
            position will close then a new position will open 
            and 1 lot will be bought.
            If the last position is open and long then nothing will happen.

            In Multiple Position regime:
            buys specified number of lots. If the last position
            was closed new position will open.
            If the last trade in a position is open and short then position
            won't close but specified number of lots will be bought.
            If the last trade in a position is open ang long then
            specified number of lots will be bought.
            Notice that volume position limited as follows:
            -MAX_AVAILABLE_VOLUME <= used_volume <= MAX_AVAILABLE_VOLUME.

            Arguments:
                volume (float): Number of lots that will be bought.

            Warns:
                warn: If specified volume is negative.
                warn: In SP regime if the last position is open and long.

            Raises:
                ValueError: In SP regime if specified volume 
                    exceeds MAX_AVAILABLE_VOLUME.
                ValueError: In MP regime if cumulative volume of positions
                    exceeds MAX_AVAILABLE_VOLUME.

            Returns:
                None

            Examples:
            ```python
                # In SP regime open a position and buy 1 lot.
                # Used volume is 1, available volume is 0.
                def onBar(instrument):
                    alg.openPosition()
                    alg.buy()
            ```
            ```python
                # In SP regime open a position and buy 1 lot.
                # Used volume is 1, available volume is 0.
                def onBar(instrument):
                    alg.openPosition()
                    alg.buy(0.1)
            ```
            ```python
                # In SP regime buy 1 lot. 
                # Position will open automatically.
                # Used volume is 1, available volume is 0.
                def onBar(instrument):
                    alg.buy()
            ```
            ```python
                # In SP regime buy 1 lot using buy()
                # then close opened long and sell 1 lot.
                def onBar(instrument):
                    alg.buy() used volume is 1, available is 0;
                    alg.sell() used volume is -1, available volume is 0.
            ```
            ```python
                # In MP regime buy 0.1 lots then buy 0.2 lots
                def onBar(instrument):
                    alg.buy(0.1) used volume is 0.1, available is 0.9;
                    alg.buy(0.2) used volume is 0.3, available volume is 0.7.
            ```
            ```python
                # In MP regime buy 0.1 lots then sell 0.2 lots
                def onBar(instrument):
                    alg.buy(0.1) used volume is 0.1, available is 0.9;
                    alg.sell(0.2) used volume is -0.1, available volume is 0.9.
            ```
        """

        if volume <= 0:
            warn("Volume must be positive! Nothing will happen!\n")
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
                        warn("Can't buy since there is an open buy!\n")
                    else:
                        self.closePosition()
                        self.openPosition()
                        self._open_trade(volume, side=1)
                else:
                    self._open_trade(volume, side=1)
            else:
                self.openPosition()
                self._open_trade(volume, side=1)
        else:
            is_closed = self._is_last_pos_closed()
            if is_closed == None or is_closed > 0:
                self.openPosition()
                self._open_trade(volume, side=1)
            else:
                volume_used = self.positions[-1].volume_used
                self.positions[-1].id
                if abs(volume_used + volume) > MAX_AVAILABLE_VOLUME:
                    s = "You use {} number of lots.".format(volume_used)+\
                        "Can't buy {} lots, since total volume".format(volume)+\
                        "will exceed the upper limit!"
                    raise ValueError(s)
                else:
                    self._open_trade(volume, side=1)
        pos_id = self.positions[-1].id
        return pos_id


    def sell(self, volume=1):
        """ Sells specified volume of an asset.

            In Single Position regime:
            sells 1 lot despite of volume received 
            by the function. If the last position
            was closed new position will open automatically.
            If the last position is open and long then this
            position will close then a new position will open 
            and 1 lot will be sold.
            If the last position is open and short then nothing will happen.

            In Multiple Position regime:
            sells specified number of lots. If the last position
            was closed new position will open.
            If the last trade in a position is open and long then position
            won't close but specified number of lots will be sold.
            If the last trade in a position is open ang shoer then
            specified number of lots will be sold.
            Notice that volume position limited as follows:
            -MAX_AVAILABLE_VOLUME <= used_volume <= MAX_AVAILABLE_VOLUME.

            Arguments:
                volume (float): Number of lots that will be sold.

            Warns:
                warn: If specified volume is negative.
                warn: In SP regime if the last position is open and short.

            Raises:
                ValueError: In SP regime if specified volume 
                    exceeds MAX_AVAILABLE_VOLUME.
                ValueError: In MP regime if cumulative volume of positions
                    exceeds MAX_AVAILABLE_VOLUME.

            Returns:
                None

            Examples:
            ```python
                # In SP regime open a position and sell 1 lot.
                # Used volume is -1, available volume is 0.
                def onBar(instrument):
                    alg.openPosition()
                    alg.sell()
            ```
            ```python
                # In SP regime open a position and sell 1 lot.
                # Used volume is -1, available volume is 0.
                def onBar(instrument):
                    alg.openPosition()
                    alg.sell(0.1)
            ```
            ```python
                # In SP regime sell 1 lot. 
                # Position will open automatically.
                # Used volume is -1, available volume is 0.
                def onBar(instrument):
                    alg.sell()
            ```
            ```python
                # In SP regime sell 1 lot using sell()
                # then close opened short and buy 1 lot.
                def onBar(instrument):
                    alg.sell() used volume is -1, available is 0;
                    alg.buy() used volume is 1, available volume is 0.
            ```
            ```python
                # In MP regime sell 0.1 lots then sell 0.2 lots
                def onBar(instrument):
                    alg.sell(0.1) used volume is -0.1, available is 0.9;
                    alg.sell(0.2) used volume is -0.3, available volume is 0.7.
            ```
            ```python
                # In MP regime sell 0.1 lots then buy 0.2 lots
                def onBar(instrument):
                    alg.sell(0.1) used volume is -0.1, available is 0.9;
                    alg.buy(0.2) used volume is 0.1, available volume is 0.9.
            ```
        """

        if volume <= 0:
            warn("Volume must be positive! Nothing will happen!\n")
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
                        warn("Can't sell since there is an open sell!\n")
                    else:
                        self.closePosition()
                        self.openPosition()
                        self._open_trade(volume, side=-1)
                else:
                    self._open_trade(volume, side=-1)
            else:
                self.openPosition()
                self._open_trade(volume, side=-1)
        else:
            volume *= -1
            is_closed = self._is_last_pos_closed()
            if is_closed == None or is_closed > 0:
                self.openPosition()
                self._open_trade(volume, side=-1)
            else:
                volume_used = self.positions[-1].volume_used
                self.positions[-1].id
                if abs(volume_used + volume) > MAX_AVAILABLE_VOLUME:
                    s = "You use {} number of lots.".format(volume_used)+\
                        "Can't sell {} lots, since total volume".format(volume)+\
                        "will exceed the upper limit!"
                    raise ValueError(s)
                else:
                    self._open_trade(volume, side=-1)
        pos_id = self.positions[-1].id
        return pos_id


    def openLong(self, volume=1):
        """ Opens a position and buys specified number of lots.

            This function combains functionality of the following code:
            ```python:
                alg.openPosition()
                alg.buy(volume)
            ```

            Arguments:
                volume (float): Number of lots that will be bought.

            Warns:
                warn: If there is opened long position

            Returns:
                None: If the last position is open and long;
                pos_id (int): Position id returned by openPosition() function.
            
            Examples:
            ```python
                # In SP regime open position and buy 1 lot.
                # Used volume is 1, available volume is 0.
                def onBar(instrument):
                    alg.openLong()
            ```
            ```python
                # In SP regime open position and buy 1 lot.
                # Used volume is 1, available volume is 0.
                def onBar(instrument):
                    alg.openLong(0.1)
            ```
            ```python
                # In MP regime open position and buy 1 lot.
                # Used volume is 1, available volume is 0.
                def onBar(instrument):
                    alg.openLong()
            ```
            ```python
                # In MP regime open position and buy 0.1 lot.
                # Used volume is 0.1, available volume is 0.9.
                def onBar(instrument):
                    alg.openLong(0.1)
            ```
        """

        pos_id = self.buy(volume)
        return pos_id


    def openShort(self, volume=1):
        """ Opens a position and sells specified number of lots.

            This function combains functionality of the following code:
            ```python:
                alg.openPosition()
                alg.sell(volume)
            ```

            Arguments:
                volume (float): Number of lots that will be sold.

            Warns:
                warn: If there is opened short position

            Returns:
                None: If the last position is open and short;
                pos_id (int): Position id returned by openPosition() function.
            
            Examples:
            ```python
                # In SP regime open position and sell 1 lot.
                # Used volume is -1, available volume is 0.
                def onBar(instrument):
                    alg.openShort()
            ```
            ```python
                # In SP regime open position and sell 1 lot.
                # Used volume is -1, available volume is 0.
                def onBar(instrument):
                    alg.openShort(0.1)
            ```
            ```python
                # In MP regime open position and sell 1 lot.
                # Used volume is -1, available volume is 0.
                def onBar(instrument):
                    alg.openShort()
            ```
            ```python
                # In MP regime open position and sell 0.1 lot.
                # Used volume is -0.1, available volume is 0.9.
                def onBar(instrument):
                    alg.openShort(0.1)
            ```
        """
        
        pos_id = self.sell(volume)
        return pos_id

    def setSL(self, loss=None):
        """ Sets the maximum loss for a position.

            After opening a position user can define the maximum
            acceptable loss. Backtest algorithm after each tick
            checks current profit of the position. If current profit
            becomes lower than specified loss value then position 
            will automatically close.

            Arguments:
                loss (float): Value of the stoploss.

            Raises:
                ValueError: If loss is not nonnegative.
            
            Returns:
                None

            Examples:
            ```python
                # Works in any regime.
                def onBar(instrument):
                    alg.buy()
                    alg.setSL(loss = 300)
            ```
        """

        is_closed = self._is_last_pos_closed()
        if not is_closed:
            if loss > 0:
                self.positions[-1].stop_loss = loss
            elif loss == 0:
                self.positions[-1].stop_loss = None
            else:
                raise ValueError("Cannot set stoploss! Stoploss can't be None")

    def setTP(self, profit=None):
        """ Sets the maximum profit for a position.

            After opening a position user can define the maximum
            acceptable profit. Backtest algorithm after each tick
            checks current profit of the position. If current profit
            becomes greater than specified profit value then position 
            will automatically close.

            Arguments:
                profit (float): Value of the takeprofit.

            Raises:
                ValueError: If profit is not nonnegative.

            Returns:
                None

            Examples:
            ```python
                # Works in any regime.
                def onBar(instrument):
                    alg.buy()
                    alg.setTP(profit = 300)
            ```
        """

        is_closed = self._is_last_pos_closed()
        if not is_closed:
            if profit > 0:
                self.positions[-1].take_profit = profit
            elif profit == 0:
                self.positions[-1].take_profit = None
            else:
                raise ValueError("Cannot set stoploss! Stoploss can't be None")

    def setSLTP(self, loss=None, profit=None):
        """ Sets stoploss and takeprofit simultaneously.

            Invoke of this function is equivalent to the following code:
            ```python
                alg.setSL(loss)
                alg.setTP(profit)
            ```

            Arguments:
                loss (float): Value of the stoploss.
                profit (float): Value of the takeprofit.
            
            Returns:
                None

            Examples:
            ```python
                # Set stoploss and takeprofit using single function.
                # Works in any regime.
                def onBar(instrument):
                    alg.buy()
                    alg.setSLTP(loss = 300, profit = 300)
                    equivalelnt to
                    alg.setSL(loss = 300)
                    alg.setTP(profit = 300)
            ```
        """

        self.setSL(loss)
        self.setTP(profit)

    def closePosition(self, id=None):
        """ Close opened position.

            Closes last opened position if id == None,
            otherwise closes position with specified id (if this position
            is open).

            Arguments:
                id (int): id of position to be closed.

            Warns:
                warn: If there is no opened position.
                warn: If position with specified id is already closed.

            Returns:
                None

            Examples:
            ```python
                # On the first bar open long position with 1 lot.
                # Close position if the last open price was greater
                # than 10000.
                def onBar(instrument):
                    alg.openLong(1)
                    if instrument.open[1] > 10000:
                        alg.closePosition()
            ```
        """

        closed = False
        if id == None:
            is_closed = self._is_last_pos_closed()
            if is_closed is not None and not is_closed:
                last_pos = self.positions[-1]
                last_pos.close_time = self.now
                side = self.getPositionSide(last_pos.id)
                if side == 1:
                    close_price = self.recent_price - self.slippage
                elif side == -1:
                    close_price = self.recent_price + self.slippage
                else:
                    raise ValueError("Position side in neither 1, nor -1!")
                last_pos.close_trades(self.now, close_price)
                last_pos.closed = True
                closed = True
                if last_pos.on_close is not None:
                    last_pos.on_close()
            else:
                warn("Can't close position! There is no opened position!\n")
        else:
            for pos in self.positions:
                if pos.id == id:
                    if pos.closed:
                        warn("Can't close position with id {}".format(id)+\
                             " because it is closed already!\n")
                    else:
                        pos.close_time = self.now
                        side = self.getPositionSide(pos.id)
                        if side == 1:
                            close_price = self.recent_price - self.slippage
                        elif side == -1:
                            close_price = self.recent_price + self.slippage
                        else:
                            raise ValueError(
                                "Position side in neither 1, nor -1!")
                        pos.close_trades(self.now, float(close_price))
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
            self.positions[-1].profit = self.positions[
                -1].calculate_final_profit()
            #self.positions[-1].profit -= (2 * volume_traded * self.slippage)

    def onPositionClose(self, pos_id, handler):
        """ Call handler right after position close.

            Invokes handler function when position with pos_id was closed.

            Arguments:
                pos_id (int): id of a position.
                handler (function): method to be invoked after position close.

            Raises:
                ValueError: If position with pos_id was not find.
                TypeError: If handler is not callable.
            
            Returns:
                None

            Examples:
            ```python
                # Works in any regime.
                pos_id = None
                def onBar(instrument):
                    global pos_id
                    pos_id = alg.openLong()
                    alg.onPositionClose(pos_id, handler)
                    alg.closePosition(pos_id)
                
                def handler():
                    print("Position closed!")
            ```
        """
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
        """ Returns available volume for trading.

            If the last position is open calculates available volume.

            Warns:
                warn: If the last position was close.

            Returns:
                None: if the last position is not open
                float: if the last position is open.
                    Notice that for available volume holds inequallity:
                    0 <= available volume <= MAX_AVAILABLE_VOLUME.

            Examples:
            ```python
                # In SP regime
                def onBar(instrument):
                    alg.buy()
                    alg.getAvailableVolume() returns 0
            ```
            ```python
                # In MP regime
                def onBar(instrument):
                    alg.buy(0.2)
                    alg.getAvailableVolume() returns 0.8
            ```
            ```python
                # In MP regime
                def onBar(instrument):
                    alg.sell(0.5)
                    alg.getAvailableVolume() returns 0.5
            ```
        """

        is_closed = self._is_last_pos_closed()
        if is_closed == False:
            return self.positions[-1].available_volume()
        else:
            warn(
                "Can't get available volume since there is no opened position!\n"
            )
            return None

    def getLastPrice(self, ticker=None):
        """ Returns last price in the backtest.

            Returns last price of the specified instrument. If instrument
            is not specified then the last price of the first added 
            instrument will return. If user added several instruments (highly
            bad practice at time) it is possible to get last price of the
            specified instrument.

            Arguments:
                ticker (str, optional): Name of the underlying asset.

            Returns:
                float: Last price of the instrument.

            Raises:
                AssertionError: If only one instrument was added by user,
                    but non-exisiting ticker was specified.
                NameError: If ticker was not found among added instruments.

            Examples:
            ```python
                # Works in any regime.
                alg = TNG(name, regime, start_date, end_date)
                alg.addInstrument("btcusd")
                alg.addTimeframe("btcusd", 10)
                def onBar(instrument):
                    alg.getLastPrice()
            ```
            ```python
                # Works in any regime.
                alg = TNG(name, regime, start_date, end_date)
                alg.addInstrument("btcusd")
                alg.addTimeframe("btcusd", 10)
                def onBar(instrument):
                    alg.getLastPrice("btcusd")
            ```
            ```python
                # Works in any regime.
                alg = TNG(name, regime, start_date, end_date)
                alg.addInstrument("btcusd")
                alg.addInstrument("ethbtc")
                alg.addTimeframe("btcusd", 10)
                alg.addTimeframe("ethbtc", 15, 30)
                def onBar(instrument):
                    alg.getLastPrice() Returns the last price of btcusd
            ```
            ```python
                # Works in any regime.
                alg = TNG(name, regime, start_date, end_date)
                alg.addInstrument("btcusd")
                alg.addInstrument("ethbtc")
                alg.addTimeframe("btcusd", 10)
                alg.addTimeframe("ethbtc", 15, 30)
                def onBar(instrument):
                    alg.getLastPrice() Returns the last price of btcusd
                    alg.getLastPrice("ethbtc")
            ```
        """

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

    def getPositionSide(self, pos_id):
        """ Docs!
        
        Arguments:
            pos_id (int) -- Id of position.
        
        Raises:
            TypeError -- If pos_id is not integer.
            ValueError -- If position with pos_id was not found.
        
        Returns:
            float -- +1., if position was long and
                     -1., if position was short
        """

        if not isinstance(pos_id, int):
            raise TypeError("Position id must be int!")
        for pos in self.positions[::-1]:
            if pos.id == pos_id:
                return sign(pos.volume_used)
        raise ValueError("Position with id {} was not found!".format(pos_id))

    def on(self, type_=None, params=None, arguments=None, handler=None):
        """ Wait for specified event and call handler.

            User can define two types of events: Price event and Time event.
            Price event:
                Wait for the specified price. At the moment when current price
                strikes specified price handler will call.
            Time event:
                Wait for the specified time. At the momene then current time
                is equal or exceeds specified time handler will call.

            Arguments:
                type_ (str): Name of the type of the event: Price or Time.
                params: For Price event -- price (float).
                    For Time event -- time (int).
                argument (tuple): Arguments for handler method.
                handler (function): method that will invoke when speicified
                    event happend.
            Returns:
                id of the event.

            Raises:
                ValueError: If type_ was not Price neither Time.

            Examples:
                ```python
                    # Works in any regime.
                    event_id = None
                    def onBar(instrument):
                        global event_id
                        event_id = alg.on("Price", 10000, handler)
                    
                    def handler():
                        print("Price event handler!")
                ```
                ```python
                    # Works in any regime.
                    event_id = None
                    def onBar(instrument):
                        global event_id
                        event_id = alg.on("Time", 20180201000000, handler)
                    
                    def handler():
                        print("Time event handler!")
                ```
        """
        ticker = list(self.ticker_timeframes)[0]
        if type_ == "Price":
            if self._check_price_params(params, handler):
                if self.recent_price <= params:
                    trigger = 1
                elif self.recent_price > params:
                    trigger = -1
                new_price_event = PriceEvent(ticker, params, trigger,
                                             arguments, handler)
                new_price_event.id = randint(2**1, 2**31 - 1)
                self.price_events.append(new_price_event)
                return new_price_event.id
        elif type_ == "Time":
            time = self._check_time_params(params, handler)
            if time is not None:
                new_time_event = TimeEvent(ticker, time, arguments, handler)
                new_time_event.id = randint(2**1, 2**31 - 1)
                self.time_events.append(new_time_event)
                return new_time_event.id
        else:
            raise ValueError("Unknown type of an event {}!".format(type_))

    def off(self, id):
        """ Disables event.

            If some event was setted by on() method, off() will cancels it.

            Arguments:
                id (int): id of the event.
            
            Returns:
                None

            Warns:
                warn: if the event with specified id was not found.

            Examples:
            ```python
                # Works in any regime.
                event_id = None
                def onBar(instrument):
                    global event_id
                    event_id = alg.on("Price", 10000, handler)
                    if alg.getLastPrice() > 10000:
                        alg.off(event_id)
                
                def handler():
                    global event_id
                    print("Price event handler!")
            ```
            ```python
                # Works in any regime.
                event_id = None
                def onBar(instrument):
                    global event_id
                    event_id = alg.on("Time", 20180201000000, handler)
                    if instrument.time > 20180201000000:
                        alg.off(event_id)
                
                def handler():
                    print("Time event handler!")
            ```
        """

        for price_event in self.price_events:
            if price_event.id == id:
                self.price_events.remove(price_event)
                return
        for time_event in self.time_events:
            if time_event.id == id:
                self.time_events.remove(time_event)
                return
        warn("Event with id {} was not found!\n".format(id))

###############################################################################
#                           Utility routines
###############################################################################
    def _check_price_params(self, params, handler):
        if isinstance(params, int) or isinstance(params, float):
            if callable(handler):
                for event in self.price_events:
                    if event.threshold == params and event.handler == handler:
                        warn("This Price event already exists!\n")
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
                        "Can't add new time event! Specified time is in past!\n"
                    )
                    return None
                for event in self.time_events:
                    if event.time == time and event.handler == handler:
                        warn("This Time event already exists!\n")
                        return None
                return time
            else:
                raise TypeError("Value in handler is not callable!")
        else:
            raise TypeError("Time must be of datetime type")

    def _is_last_pos_closed(self):
        """ Returns status of the last position.

        Returns:
            int: last position id if last position is closed;
            bool: False if last position is open;
            None: if there is no last position.
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
            trade_id = randint(2**1, 2**31 - 1)
        if side == 1:
            open_price = self.recent_price + self.slippage
        elif side == -1:
            open_price = self.recent_price - self.slippage
        new_trade = Trade(trade_id, open_price, volume, self.now)
        if self.positions and self.positions[-1].trades:
            last_trade = self.positions[-1].trades[-1]
            if not last_trade.close_time:
                last_trade.close_time = self.now
                last_trade.close_price = self.recent_price
        self.positions[-1].trades.append(new_trade)
        self.positions[-1].volume_used += volume
        return trade_id
