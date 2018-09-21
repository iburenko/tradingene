from tng.algorithm_backtest.tng import TNG
from datetime import datetime
import tng.backtest_statistics.backtest_statistics as bs
from tng.algorithm_backtest.export import Export

def on_bar(instrument):
    #Code your strategy here!

name = "Cornucopia"
regime = "SP"
start_date = datetime(2018, 9, 1)
end_date = datetime(2018, 9, 4)
ticker = "btcusd"
timeframe = 60
alg = TNG(name, regime, start_date, end_date)
alg.addInstrument(ticker)
alg.addTimeframe(ticker, timeframe)

alg.run_backtest(on_bar)
new_stat = bs.BacktestStatistics(alg)
new_stat.backtest_results(plot=True)

inds = {'sma':(5), 'ema':(), 'roc':(4)}
lookback = 2
exp = Export(alg).export_results(inds, lookback)