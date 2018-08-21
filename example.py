import tng.algorithm_backtest.tng as tng
from datetime import datetime
from time import time
import tng.backtest_statistics.backtest_statistics as bs
from tng.plot.plot import plot_cs_prof
import pandas as pd
import numpy as np

name = "Cornucopia"
regime = "MP"
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 1, 15)
timeframe = 60

alg = tng.TNG(name, regime, start_date, end_date)
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", timeframe)

# df = pd.DataFrame(columns = ['time', 'open', 'high', 'low', 'close', 'vol'])
in_pos = 0
pos_id = None

def onBar(instrument):
    global in_pos, pos_id
    bollinger10 = instrument.bollinger(10)
    vol = alg.getAvailableVolume()
    if vol is None:
        vol = 666
    if instrument.close[1] > bollinger10.top[1]:
        if vol >= 0.1:
            if in_pos >= 0:
                pos_id = alg.buy(0.1)
                in_pos = 1
            else:
                alg.closePosition(pos_id)
                pos_id = alg.buy(0.1)
                in_pos = 1
        else:
            if in_pos <= 0:
                alg.closePosition(pos_id)
    if instrument.close[1] < bollinger10.bottom[1]:
        if vol >= 0.1:
            if in_pos <= 0:
                pos_id = alg.sell(0.1)
                in_pos = -1
            else:
                alg.closePosition(pos_id)
                pos_id = alg.sell(0.1)
                in_pos = -1
        else:
            if in_pos >= 0:
                alg.closePosition(pos_id)
    #print(instrument.time)
    # print(instrument.ema(3))
    # print("ad = ", instrument.ad()[1])
    # print("adx = ", instrument.adx().adx[1])
    # print("apo = ", instrument.apo()[1])
    # print("aroon = ", instrument.aroon().up[1])
    # print("atr = ", instrument.atr()[1])
    # print("bollinger = ", instrument.bollinger().top[1])
    # print("cci = ", instrument.cci()[1])
    # print("chande = ", instrument.chande()[1])
    # print("ema = ", instrument.ema(9)[1], instrument.close[1])
    # print("keltner = ", instrument.keltner().basis[1])
    # print("macd = ", instrument.macd().macd[1])
    # print("momentum = ", instrument.momentum()[1])
    # print("ppo = ", instrument.ppo()[1])
    # print("roc = ", instrument.roc()[1])
    # print("sma = ", instrument.sma()[1])
    # print("rsi = ", instrument.rsi()[1])
    # print("stochastic = ", instrument.stochastic().k[1])
    # print("trima = ", instrument.trima()[1])
    # print("williams = ",instrument.williams()[1])
    # print("======================================")
    # if instrument.open[1] > instrument.close[1]:
    #     # If price goes down during the day then sell;
    #     alg.sell()
    # elif instrument.open[1] < instrument.close[1]:
    #     # If price goes up during the day then buy;
    #     alg.buy()
    # else:
    #     # If price did not change then do nothing;
    #     pass


alg.run_backtest(onBar)
new_stat = bs.BacktestStatistics(alg)
new_stat.backtest_results()