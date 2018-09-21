from tng.algorithm_backtest.tng import TNG
from datetime import datetime
import tng.backtest_statistics.backtest_statistics as bs
from tng.algorithm_backtest.export import Export

def on_bar(instrument):
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
    elif entry == 1:
        if (instrument.high[1] / instrument.high[2] < 1
                and instrument.low[1] / instrument.low[2] < 1):
            alg.sell()
            entry = -1
            return
    elif entry == -1:
        if (instrument.high[1] / instrument.high[2] > 1
                and instrument.low[1] / instrument.low[2] > 1):
            alg.buy()
            entry = 1
            return

name = "Cornucopia"
regime = "SP"
start_date = datetime(2018, 9, 1)
end_date = datetime(2018, 9, 4)
ticker = "btcusd"
timeframe = 60
alg = TNG(name, regime, start_date, end_date)
alg.addInstrument(ticker)
alg.addTimeframe(ticker, timeframe)
entry = 0
signal = 0

alg.run_backtest(on_bar)
new_stat = bs.BacktestStatistics(alg)
new_stat.backtest_results(plot=True)
print(new_stat.PnL)
inds = {'adx':(5), 'atr':(7), 'roc':(7)}
lookback = 2
exp = Export(alg).export_results(inds, lookback)