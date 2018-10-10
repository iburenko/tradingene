from numpy import sign
from tng.algorithm_backtest.trade import Trade

class CheatPosition:


    def __init__(self, price, volume, now, calculate_fee):
        self.open_price = price
        self.close_price = 0
        self.open_time = now
        self.close_time = 0
        self.volume = volume
        self.side = sign(volume)
        self.closed = False
        self.trades = [Trade(self.side, price, volume, now)]
        self.profit = 0
        self.calculate_fee = calculate_fee
        self.fee = .0
        if calculate_fee:
            self.fee = price * 0.002


    def close_position(self, price, time_):
        self.close_price = price
        self.close_time = time_
        self.closed = True
        self.profit = self.side * (self.close_price - self.open_price)
        self.trades[0].close_price = price
        self.trades[0].close_time = time_
        if self.calculate_fee:
            self.fee += (price * 0.002)
      


        