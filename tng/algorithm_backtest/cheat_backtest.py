from datetime import datetime, timedelta
from tng.data.load import import_candles
from tng.algorithm_backtest.cheat_position import CheatPosition
import tng.algorithm_backtest.limits as limits


class CheatBacktest:
    def __init__(self, ticker, timeframe, start_date, end_date, indicators):
        self.ticker = ticker
        self.timeframe = timeframe
        self.start_date = start_date - timedelta(minutes=50*self.timeframe)
        self.end_date = end_date
        self.indicators = indicators
        self.data = self._load_data()
        self.positions = list()
        self.iter = 51
        self.slippage = 0
        self.calculate_fees = False

    
    def _load_data(self):
        data = import_candles(
            self.ticker, 
            self.timeframe, 
            self.start_date, 
            self.end_date, 
            indicators=self.indicators
        )
        return data


    def buy(self, volume=1):
        last_candle = self.data.iloc[-self.iter]
        price = last_candle.open + self.slippage
        time_ = int(last_candle.time)
        fee = self.calculate_fees
        if self.positions:
            if self.positions[-1].closed:
                pos = CheatPosition(price, volume, time_, fee)
            else:
                if self.positions[-1].side == 1:
                    return
                else:
                    self.positions[-1].close_position(price, time_)
                    pos = CheatPosition(price, volume, time_, fee)
        else:
            pos = CheatPosition(price, volume, time_, fee)
        self.positions.append(pos)
        

    def sell(self, volume=1):
        volume *= -1
        last_candle = self.data.iloc[-self.iter]
        price = last_candle.open - self.slippage
        time_ = int(last_candle.time)
        fee = self.calculate_fees
        if self.positions:
            if self.positions[-1].closed:
                pos = CheatPosition(price, volume, time_, fee)
            else:
                if self.positions[-1].side == -1:
                    return
                else:
                    self.positions[-1].close_position(price, time_)
                    pos = CheatPosition(price, volume, time_, fee)
        else:
            pos = CheatPosition(price, volume, time_, fee)
        self.positions.append(pos)


    def closePosition(self):
        if self.positions:
            last_pos = self.positions[-1]
            if not last_pos.closed:
                last_candle = self.data.iloc[-self.iter]
                price = last_candle.open
                time_ = int(last_candle.time)
                if last_pos.side == 1:
                    price -= self.slippage
                else:
                    price += self.slippage
                self.positions[-1].close_position(price, time_)


    def _set_slippage(self):
        ticker = self.ticker
        if ticker == "btcusd":
            self.slippage = limits.BTCUSD_SLIPPAGE
        elif ticker == "ethusd":
            self.slippage = limits.ETHUSD_SLIPPAGE
        elif ticker == "ltcusd":
            self.slippage = limits.LTCUSD_SLIPPAGE
        elif ticker == "ethbtc":
            self.slippage = limits.ETHBTC_SLIPPAGE
        elif ticker == "ltcbtc":
            self.slippage = limits.LTCBTC_SLIPPAGE
        elif ticker == "dshbtc":
            self.slippage = limits.DSHBTC_SLIPPAGE
        elif ticker == "xrpbtc":
            self.slippage = limits.XRPBTC_SLIPPAGE
        else:
            raise NameError("slippage cannot be set, unknown ticker!")


    def run_backtest(self, on_bar, slippage=True, fees=False):
        if slippage:
            self._set_slippage()
        if fees:
            self.calculate_fees = True
        for self.iter in range(51, len(self.data)):
            on_bar(self.data[-self.iter:])

        
    def reset_backtest(self):
        self.positions = list()
        self.iter = 51