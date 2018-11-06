#Backtest results

After you have run ```alg.run_backtest(onBar)``` you are able to analyze the performance of your algorithm. To do this you need to initialize an instance of the ```BacktestStatistics``` class passing ```alg``` as a parameter for the initializer:

```python
from datetime import datetime
from tradingene.algorithm_backtest.tng import TNG
from tradingene.backtest_statistics import backtest_statistics as bs

############################################################
# here goes code of your algorithm
############################################################

stats = bs.BacktestStatistics(alg)
```

Class ```BacktestStatistics``` comprises methods that calculate algorithm's specific statistics. For instance if you wish to calculate cumulative profit (or profit and loss) and the overall number of trades of a backtest you write:

```python
stats = bs.BacktestStatistics(alg)
pnl = stats.calculate_PnL()
number_of_trades = stats.calculate_number_of_trades()
```

[_See full list of methods_](all_stats_methods.md)

If you want to calculate all available statistics with a single method, use ```backtest_results```:

```python
stats = bs.BacktestStatistics(alg)
stats.backtest_results(plot=True, filename="backtest_stats")
```
