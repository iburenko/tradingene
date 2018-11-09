from datetime import datetime
from tradingene.data.load import import_data
from tradingene.algorithm_backtest.tng import TNG
import tradingene.backtest_statistics.backtest_statistics as bs

START_DATE = datetime(2018, 1, 1) # The first day of simulated trading period
END_DATE = datetime(2018, 2, 1) # The last day of simulated trading period
TICKER = "btcusd" # A ticker to use
TIMEFRAME = 60 # A timeframe to use

def onBar(instrument):
    bollinger10 = instrument.bollinger(10) # Retrieving the value of the Bollinger indicator of period 10.
    if instrument.close[1] > bollinger10.top[1]: # If the price soars above the Bollinger top line...
        _alg.buy() # ...buying.
    elif instrument.close[1] < bollinger10.bottom[1]: # If the price falls below the Bollinger bottom line... 
        _alg.sell() # ... selling.

_alg = TNG(START_DATE, END_DATE) # Creating an instance of the class (TNG) to run the algorithm within.
_alg.addInstrument(TICKER) # Adding an instrument.
_alg.addTimeframe(TICKER, TIMEFRAME) # Adding a time frame. 
_alg.run_backtest(onBar) # Backtesting...

stat = bs.BacktestStatistics(_alg) # Retrieving statistics of the backtest

pnl = stat.calculate_PnL()
num_positions = stat.calculate_number_of_trades()
print("pnl=%f, num_positions=%d" % (pnl, num_positions) )

stat.backtest_results() # Displaying the backtest statistics
