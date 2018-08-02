import tng.algorithm_backtest.tng as tng
from datetime import datetime
from time import time
import tng.backtest_statistics.backtest_statistics as bs
from tng.plot.plot import plot_cs_prof

name = "Cornucopia"
regime = "MP"
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 2, 1)

alg = tng.TNG(name, regime, start_date, end_date)
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 60)

timeframe = 60

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

alg.run_backtest(onBar)

for pos in alg.positions:
    for trade in pos.trades:
        print(trade.open_time, trade.open_price, trade.close_time,
            trade.close_price, trade.side)
    print("------------------ end of pos -------------------")

new_stat = bs.BacktestStatistics(alg.positions)
new_stat.backtest_results()

plot_cs_prof(alg, timeframe)
