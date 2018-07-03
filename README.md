# Tradingene package for backtesting algorithms.

![alt text][logo]

[logo]: https://github.com/iburenko/tng/blob/master/logo_tg_large_1stroke.png "Tradingene.com"

## Overview

This package is project of [Tradingene.com](https://tradingene.com/) team.
It was developed for stand-alone backtesting of trading algorithms mimicking
Tradingene's API (see documentaion [here](https://lk.tradingene.com/doc)).

***

Our package allows you to test your trading ideas. You write a code that reflects your trading logic and after backtest you are able to check whether your idea was good or not based on our backtest statistics. The best algorithms will have an opportunity to run live on an exchange (see [Tradingene.com](https://tradingene.com/) web site).

***

At the moment this package is able to mimic Tradingene's API, but very soon it will be possible to test your strategies using **machine learning** algorithms!

***
## Getting started

_Notice_: There are little differences in a preparation stage between web platform and this package while setting up all needed parameters. We will explain here only package's setting. Platform setting is a little bit easier due to user interface.

All needed functionality is contained in a TNG class, class constructor takes 4 parameters (in the order of appearance):
1. Name of the algorithm (string);
2. Trading regime ("SP" or "MP", to be explained further)
3. Date that backtest starts (datetime);
4. Date that backtest ends (datetime).

> **If you don't know what class and/or constructor is -- don't worry!** It is easy to follow the logic and meaning of this variables, particular implementation is not important!

Fisrt you have to specify name of your algorithm, regime that algorithm will use, start and end of backtest (other possible initializations see [here](where?)).

```python
from tng
from datetime import datetime

name = "Cornucopia"
regime = "SP"
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 2, 1)

alg = tng.TNG(name, regime, start_date, end_date)
```

After this code you will code an object named ```alg```, which contains all the functions you need. When you will run backtest your algorithm will be simulated from the January 1st 2018 till February 1st 2018.

***

After initialization like above you are able to add instrument and timeframe to your algorithm.

```python
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 1440)
```

Instrument is the name of the asset that your algorithm will use. Timeframe is measured in minutes. In the example above user-defined onBar function will call every 1440 minutes (one day) if there is a fully formed candle. _Please see detailed explanation see [here](where??)._

***

The next step is to implement onBar function. This function contains the core idea of your algorithm. Trading idea in this example is very clear.

1. If the daily price moved down we sell hoping that this falling will continue;
2. If the daily price raised during the day we buy hoping that the price will continue to go up;
3. If an open price is equal to a close price do nothing;
4. If several raising (falling) candles appears in a row then algorithm will buy (sell) only on the first candle (you will see a warning);
5. If you are in a short position after buy you will have long position and vice versa.

In this example you are always "in a position", what position you have depends on the last daily candle.

Code that implements trading logic described above:

```python
def onBar(instrument):
    if instrument.open[1] > instrument.close[1]:
        # If price goes down during the day then sell;
        alg.sell()
    elif instrument.open[1] < instrument.close[1]:
        # If price goes up during the day then buy;
        alg.buy()
    else:
        # If price did not change then do nothing
        pass
```

This trading logic is very easy though you can find more [example here](where are examples).
***

After all needed steps are done we are able to backtest our strategy finally! Idea behind backtest is easy: backtest goes through historical data and invokes user-defined onBar function after ```timeframe``` (specified in a ```addTimeframe``` function) minutes left.

Backtest your algorithm like this:

```python
alg.run_backtest(onBar)
```

That's it! Now you can see results of your backtest (not implemented yet)!
