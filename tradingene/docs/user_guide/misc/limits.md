There are several predefined constants which a user is able to change. But one should do it carefully taking in account that it might change result of the backtest comparing to the backtest on the [Tradingene.com](https://tradingene.com) platform.

All limits are described in file ```tradingene_package/algorithm_backtest/limits.py```

## Slippage constants:

When you open or close a trade or position price will be changed against user due to slippage.

|Instrument|Slippage|
|:---:|:---:|
|BTCUSD|1e0|
|ETHUSD|1e-1|
|LTCUSD|1e-2|
|ETHBTC|1e-6|
|LTCBTC|1e-6|
|DSHBTC|1e-6|
|XRPBTC|1e-9|

## Lookback period

Constant which controls length of history available in ```instrument``` in ```onBar()``` method.

Default value:

```LOOKBACK_PERIOD = 50```

## Backtest constants

It is not able to get history data before EARLIEST_START:

```EARLIEST_START = datetime(2017, 1, 1)```

Volume available in position controls by ```MAX_AVAILABLE_VOLUME``` constant:

```MAX_AVAILABLE_VOLUME = 1```
