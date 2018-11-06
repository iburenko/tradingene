### Using multiple positions

Along with ```buy()``` and ```sell()``` the Tradingene framework provides you with more tools for making trades including ```openLong()``` and ```openShort()``` functions. With these ones you may have two positions of opposite side opened at the same time. Opening a "counter-trade" while holding another one still opened may serve several purposes, e.g. temporarily hedging while surviving a drawdown, saving commission expanses payed to exchange etc.

When opening a trade with either ```openLong()``` or ```openShort()``` you must specified the number of lots to use:
```python
	long_position = alg.openLong(1) # ...buying 1 lot.
```
The function returns the identifier of a position just been opened. We may use this identifier to control position in the future. For example we may specify a function to be called when the position is closed:
```python
	alg.onPositionClose(long_position, onLongPositionClose) # Specifying the function to be called when the position is
```

A sample script is presented below.

```python
from datetime import datetime
from tradingene.data.load import import_data
from tradingene.algorithm_backtest.tng import TNG
import tradingene.backtest_statistics.backtest_statistics as bs

START_DATE = datetime(2018, 1, 1) # The first day of simulated trading period
END_DATE = datetime(2018, 2, 1) # The last day of simulated trading period
TICKER = "btcusd" # A ticker to use
TIMEFRAME = 60 # A timeframe to use

short_position = None # To save ids of short positions opened throughout backtest.
long_position = None # To save ids of short positions opened throughout backtest.

def onShortPositionClose(): # This function is called when a short position is being closed
	global short_position
	short_position = None # Resetting since no opened position exists now...


def onLongPositionClose(): # This function is called when a long position is being closed
	global long_position
	long_position = None # Resetting since no opened position exists now...


def onBar(instrument):
	global short_position, long_position

	bollinger10 = instrument.bollinger(10) # Retrieving the value of the Bollinger indicator of period 10.
	atr10 = instrument.atr(10) # Retrieving the value of the ATR indicator of period 10.
	if instrument.close[1] > bollinger10.top[1]: # If the price rises above the Bollinger top line...
		if long_position is None: # ... and if there is no opened long position yet...
			long_position = alg.openLong(1) # ...buying 1 lot.
			if long_position is not None:
				alg.setSLTP(loss=atr10[1]*2, profit=atr10[1]*2) # Setting stop loss and take profit
				alg.onPositionClose(long_position, onLongPositionClose) # Specifying the function to be called when the position is being closed
	elif instrument.close[1] < bollinger10.bottom[1]: # If the price falls below the Bollinger bottom line...
		if short_position is None: # ... and if there is no opened short position yet...
			short_position = alg.openShort(1) # ... selling 1 lot.
			if short_position is not None:
				alg.setSLTP(loss=atr10[1]*2, profit=atr10[1]*2) # Setting stop loss and take profit
				alg.onPositionClose(short_position, onShortPositionClose) # Specifying the function to be called when the position is being closed

alg = TNG(START_DATE, END_DATE) # Creating an instance of the class (TNG) to run the algorithm within.
alg.addInstrument(TICKER) # Adding an instrument.
alg.addTimeframe(TICKER, TIMEFRAME) # Adding a time frame.
alg.run_backtest(onBar) # Backtesting...

stat = bs.BacktestStatistics(alg) # Retrieving statistics of the backtest

pnl = stat.calculate_PnL()
num_positions = stat.calculate_number_of_trades()
print("pnl=%f, num_positions=%d" % (pnl, num_positions))

stat.backtest_results() # Displaying the backtest statistics
```
