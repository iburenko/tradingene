# Tradingene's package for backtesting trading algorithms

![image](img/logo_tg_large_1stroke.png)

Tradingene allows you to write and backtest strategies written in Python. You can easily rewrite your code if you want to use it on the Tradingene's platform for live trading.

## Installation
Tradingne can be installed via pip for python3:

    pip3 install tradingene

## Getting Started

An algorithm represents some trading logic. Trading logic is reflected in a some user defined method. If one wants to test profitability of this logic one needs to perform backtest which consists of consequent calls of a user defined function.

---
Suppose we have the following trading logic:

  - take a long position if a close price of a bar was greater than open price;
  - take a short position if a close price of a bar was less than open price;
  - do not change position otherwise.

To start code the algorithm from above we need to define _name_, _regime_ of the algorithm and _start_date_ and _end_date_ of backtest:

### Setting parameters

```python
from datetime import datetime
from tradingene.algorithm_backtest.tng import TNG
from tradingene.backtest_statistics import backtest_statistics as bs
name = "Cornucopia"
regime = "SP"
start_date = datetime(2018, 9, 1)
end_date = datetime(2018, 10, 1)
```

After that we are ready to create an instance of the class ```TNG```. The instance ```alg``` will contain all functions that needed for backtest.

```python
alg = TNG(name, regime, start_date, end_date)
```
[_See  more on initialization_](user_guide/misc/initialization.md).

 After that we are able to specify an instrument and timeframe (measured in minutes) that we will use in our backtest:

```python
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 1440)
```
[_See  more on adding instruments and timeframes_](user_guide/misc/import_instruments.md).

### Implementing trading logic

In the next step we will implement ```onBar()``` function that will reflect our trading logic from above:

```python
def onBar(instrument):
  if instrument.open[1] > instrument.close[1]:
    # If the price moved down we take a short position
    alg.sell()
  elif instrument.open[1] < instrument.close[1]:
    # If the price moved up we take a long position
    alg.buy()
  else:
    # If the price did not change then do nothing
    pass
```

Values of technical indicators or for instance open prices contained in the variable ```instrument```.

[_See more on onBar function_](user_guide/misc/onbar.md).

Now we are ready to run backtest:
```python
alg.run_backtest(onBar)
```

### Results of backtest

After backtest is complete it is possible to get some statistics that describes a performance of your algorithm:

```python
stats = bs.BacktestStatistics(alg)
stats.backtest_results(plot=True, filename="backtest_stats")
```

These lines will generate you an html file called ```backtest_stats.html``` with backtest statistics and draw a plot with cumulative profit like am image below:

![image](img/profit_plot.png)

[_See more on backtest statistics_](user_guide/backtest_statistics/backtest_results.md).

## Machine learning and loading data

One powerful ability of ```tradingene``` package is the ability to load and operate on data for creating machine learning based algorithms.

See examples of using neural networks for [classification]() and [regression]() problems or an example with [SVM]().

 See more on [loading data](user_quide/misc/loading_data.md).
