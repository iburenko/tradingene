from tng.algorithm_backtest.tng import TNG
from datetime import datetime
from time import time
# import cProfile
# import pstats
import tng.backtest_statistics.backtest_statistics as bs

name = "my_name"
regime = "SP"

start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 1, 3)

alg = TNG(name, regime, start_date, end_date)

alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 10)

entry = 0
signal = 0


def on_bar(instrument):
    print(instrument.time)
    global entry
    global signal
    if entry == 0:
        if (instrument.high[1] / instrument.high[2] < 1
                and instrument.low[1] / instrument.low[2] < 1):
            alg.sell()
            entry = -1
            return
        elif (instrument.high[1] / instrument.high[2] > 1
              and instrument.low[1] / instrument.low[2] > 1):
            alg.buy()
            entry = 1
            return
    ############################### old version ################################
    elif entry == 1:
        if (instrument.high[1] / instrument.high[2] < 1
                and instrument.low[1] / instrument.low[2] < 1):
            #alg.closePosition()
            alg.sell()
            entry = -1
            return
    elif entry == -1:
        if (instrument.high[1] / instrument.high[2] > 1
                and instrument.low[1] / instrument.low[2] > 1):
            #alg.closePosition()
            alg.buy()
            entry = 1
            return


# cProfile.run('alg.run_backtest(on_bar)', 'profiler')
# stat = pstats.Stats('profiler')
# stat.sort_stats('time').print_stats(5)
alg.run_backtest(on_bar)

for pos in alg.positions:
    for trade in pos.trades:
        print(trade.open_time, trade.open_price, trade.close_time,
              trade.close_price)

new_stat = bs.BacktestStatistics(alg.positions)
new_stat.backtest_results()