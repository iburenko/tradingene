from tng.algorithm_backtest.limits import MAX_AVAILABLE_VOLUME


class Position:
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
        return MAX_AVAILABLE_VOLUME - abs(self.volume_used)

    def calculate_profit(self, recent_price):
        profit = 0
        if self.trades:
            for trade in self.trades:
                profit += trade.volume * (recent_price - trade.open_price)
        return profit

    @staticmethod
    def check_sltp(obj):
        try:
            assert obj.positions
            if obj.positions[-1].closed:
                return None
            else:
                last_pos = obj.positions[-1]
                pos_profit = last_pos.calculate_profit(obj.recent_price)
                last_pos.profit = pos_profit
                if last_pos.stop_loss is not None:
                    if pos_profit < -last_pos.stop_loss:
                        last_pos.profit = -last_pos.stop_loss
                        obj.close_position()
                if last_pos.take_profit is not None:
                    if pos_profit > last_pos.take_profit:
                        last_pos.profit = last_pos.take_profit
                        obj.close_position()
        except AssertionError:
            return None
