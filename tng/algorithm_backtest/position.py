from tng.algorithm_backtest.limits import MAX_AVAILABLE_VOLUME


class Position:
    """ Stores all the information about opened position.

        Arguments:
            id (int): Id of the position.
            ticker (str): Name of the underlying asset.
            now (int): Timestamp that indicates when position was opened.

        Attributes:
            id (int): id of the position. The first position has random int
                id. Next position has id increased by one.
            ticker (str): Name of the asset.
            open_time (int): Time at which position was open.
            close_time (int): Time at which position was close. close_time
                is 0 if a position is not closed.
            volume_used (float): Volume that used at the moment. The follwing
                holds:
                -MAX_AVAILABLE_VOLUME <= volume_used <= MAX_AVAILABLE_VOLUME.
            stop_loss (float): Maximum possible loss for the position.
                If position's losses exceeds this parameter position will 
                automatically close.
            take_profit (float): Maximum possible profit for the position. 
                If position's profits exceeds this parameter position will
                automatically close.
            closed (bool): Flag that indicates whether position
                is closed or not.
            trades (list): List of instances of class Trade.
                In SP regime each position will have at most one trade.
                In MP regime each position may have unlimited number of trades.
            profit (float): Current profit of the position.
            on_close (function): Function that will invoke right after closing
                of the position.
    """

    def __init__(self, id, ticker, now):
        self.id = id
        self.ticker = ticker
        self.open_time = now
        self.close_time = 0
        self.volume_used = 0
        self.stop_loss = None
        self.take_profit = None
        self.closed = False
        self.trades = list()
        self.profit = 0
        self.on_close = None

    def available_volume(self):
        """ Calculates available volume and retuns it. """
        return MAX_AVAILABLE_VOLUME - abs(self.volume_used)

    def calculate_recent_profit(self, recent_price):
        """ Calculates recent profit and returns it. """
        profit = 0
        if self.trades:
            for trade in self.trades:
                profit += trade.volume * (recent_price - trade.open_price)
        return profit

    def calculate_final_profit(self):
        profit = 0
        if self.trades:
            for trade in self.trades:
                profit += trade.volume * (trade.close_price - trade.open_price)
        return profit

    def close_trades(self, close_time_, close_price_):
        """ Stores time of close of the position, returns None. """
        for trade in self.trades:
            trade.close_time = close_time_
            trade.close_price = close_price_

    @staticmethod
    def check_sltp(obj):
        """ Checks whether stop_loss or take_profit was reached. 

            If an algorithm has opened positions on each tick of the backtest
            this method is invoke. It checks whether the current profit
            reached stop_loss or take_profit level. If not (or there none
            stop_loss and take_profit) then nothing happens, if one of these
            levels reached then position will close by closePosition() method.

            Arguments:
                obj (TNG): TNG instance.
        """

        try:
            assert obj.positions
            if obj.positions[-1].closed:
                return None
            else:
                last_pos = obj.positions[-1]
                pos_profit = last_pos.calculate_recent_profit(obj.recent_price)
                last_pos.profit = pos_profit
                if last_pos.stop_loss is not None:
                    if pos_profit < -last_pos.stop_loss:
                        side = obj.getPositionSide(last_pos.id)
                        if side == 1:
                            obj.recent_price = (
                                (-last_pos.stop_loss + last_pos.volume_used *
                                 last_pos.trades[0].open_price) /
                                last_pos.volume_used - obj.spread, 0)
                        elif side == -1:
                            obj.recent_price = (
                                (last_pos.stop_loss - last_pos.volume_used *
                                 last_pos.trades[0].open_price) /
                                (-last_pos.volume_used) + obj.spread, 0)
                        obj.closePosition()
                if last_pos.take_profit is not None:
                    if pos_profit >= last_pos.take_profit:
                        side = obj.getPositionSide(last_pos.id)
                        if side == 1:
                            obj.recent_price = (
                                (last_pos.take_profit + last_pos.volume_used *
                                 last_pos.trades[0].open_price) /
                                last_pos.volume_used - obj.spread, 0)
                        elif side == -1:
                            obj.recent_price = (
                                (-last_pos.take_profit - last_pos.volume_used *
                                 last_pos.trades[0].open_price) /
                                (-last_pos.volume_used) + obj.spread, 0)
                        obj.closePosition()
        except AssertionError:
            return None
