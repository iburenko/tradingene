The most important part of the script is the ```onBar``` function where you implement a trading logic. This section explains how ```onBar``` is called during backtesting and what data you are able to obtain inside ```onBar```.

## Backtest procedure

Suppose you engaged 5-minutes timeframe to some instrument:

```python
from datetime import datetime
from tradingene.algorithm_backtest.tng import TNG
start_date = datetime(2017, 1, 2)
end_date = datetime(2017, 1, 3)
alg = TNG("Cornucopia", "SP", start_date, end_date)
alg.addInstrumnt("ethbtc")
alg.addTimeframe("ethbtc", 5)
```

The backtest starts at ```2017-01-02 00:00:00``` and aggregates all the data from ```2017-01-02 00:00:00``` to ```2017-01-02 00:05:00``` to form the first 5-minute candle. Next the backtest waits for the first tick to come after ```2017-01-02 00:05:00``` and at the moment it appears ```onBar``` is invoked. After that the backtest aggregates all the data from ```2017-01-02 00:05:00``` to ```2017-01-02 00:10:00``` and at the moment the first tick comes after ```2017-01-02 00:10:00``` ```onBar``` is invoked.  Notice that it could take some time to wait for a tick after which ```onBar``` is invoked.

In this example the second call of the ```onBar``` method is delayed till ```2017-01-02 00:17:00``` because no data have come in the period between ```2017-01-02 00:08:00``` and ```2017-01-02 00:17:00```. The next 5-minute candle starts at ```2017-01-02 00:15:00``` and ends at ```2017-01-02 00:20:00```.

## Available data

While backtesting the following data are available: OHLC data, volumes and user demanded indicators values. All data are stored in the ```instrument``` variable. If you wish to get the 50 latest opening prices you have to write:

```python
def onBar(instrument):
  open_prices = instrument.open
```

The values related to the last fully formed candle have index 1. The candle that was formed right before has index 2 and so forth. Index 0 is reserved for the candle that has just been opened. Its opening, high, low and closing prices are the same, the volume is 0.

See more on [indexing](../indicators/how_to_address_indicator_values.md).

```python
def onBar(instrument):
  # To print the opening time of the last fully formed candle
  # and OHLC prices and volume.
  print(
        instrument.time[1],
        instrument.open[1],
        instrument.high[1],
        instrument.low[1],
        instrument.close[1],
        instrument.vol[1]
    )

  # Print time, OHLC, volume of the beginning of the candle that just started to form
  print(
        instrument.time[0],
        instrument.open[0],
        instrument.high[0],
        instrument.low[0],
        instrument.close[0],
        instrument.vol[0]
    )
```

Outputs:

```python
# On the first iteration:
20170102000000 8.22 8.22 8.22 8.22 165.045
20170102000500 8.2259 8.2259 8.2259 8.2259 0.0

# On the second iteration:
20170102000500 8.2259 8.2259 8.2049 8.2049 15.698329000000001
20170102001500 8.191 8.191 8.191 8.191 0.0
```

You have access to the latest 50 candles. Nevertheless this number can be [changed](limits.md), you should **do it carefully!**

### List of available attributes

* (list) time
* (list) open
* (list) high
* (list) low
* (list) close

You are able to obtain values of technical indicators as follows:

```python
def onBar(instrument):
  sma10 = instrument.sma(10)
  print(sma10)[1]
```

Outputs:
```python
# On the first iteration:
8.17079

# On the second iteration:
8.175180000000001
```

Indexing rules are the same as for OHLC data. List of available technical indicators see [here](../indicators/indicators_main.md).
