### First algorithm

The algorithm you learn first is rather simple and utilizes neither of machine learning methods. It serves to demonstrate you the very basics of simulated trading with the Tradingene framework.    

Basically you must do two things:  
1. Implement an ```onBar``` function to code your trading logic in.
2. Create and "launch" an instance of the ```TNG``` class that actually perform simulated trading.  

To open trades you may utilize ```buy()``` and ```sell()``` functions. Each one takes effect only if neigther trade has been opened in the same side. If a trade has already been opened in the opposite side, it would be closed.      
The trading logic used for this algorithm utilizes a well-known technical strategy: it buys when price rises above the Bollinger upper line and sells when price falls beneath the Bollinger lower line.

```python
    if instrument.close[1] > bollinger10.top[1]: # If the price soars above the Bollinger top line...
        alg.buy() # ...buying.
```

To run a backtest we must first specify the dates when it starts and finishes as well as load data for the chosen ticker and timeframe. This is done with the following lines of code:
```python
alg = TNG(START_DATE, END_DATE) # Creating an instance of the class (TNG) to run the algorithm with.
alg.addInstrument(TICKER) # Adding an instrument.
alg.addTimeframe(TICKER, TIMEFRAME) # Adding a time frame.
alg.run_backtest(onBar) # Backtesting...
```  

The whole script is presented below.

```python
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
        alg.buy() # ...buying.
    elif instrument.close[1] < bollinger10.bottom[1]: # If the price falls below the Bollinger botto line...
        alg.sell() # ... selling.

alg = TNG(START_DATE, END_DATE) # Creating an instance of the class (TNG) to run the algorithm within.
alg.addInstrument(TICKER) # Adding an instrument.
alg.addTimeframe(TICKER, TIMEFRAME) # Adding a time frame.
alg.run_backtest(onBar) # Backtesting...

stat = bs.BacktestStatistics(alg) # Retrieving statistics of the backtest

pnl = stat.calculate_PnL()
num_positions = stat.calculate_number_of_trades()
print("pnl=%f, num_positions=%d" % (pnl, num_positions) )

stat.backtest_results() # Displaying the backtest statistics
```
