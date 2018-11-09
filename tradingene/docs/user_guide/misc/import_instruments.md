# Overview

To run a backtest you must add instrument(s) and timeframe(s) to an instance
of the ```TNG``` class. For the moment it is possible to use only one instrument while backtesting. Multiple instruments will be available in the future versions.
The number of timeframes is unlimited. See details below.

## addInstrument

Adds specified instrument to an algorithm.

**Important:** Notice that at the moment backtest does
not support several instruments, so **do
not add several instruments**.

**Arguments:**

* ticker (str): Name of the underlying asset.

**Warns:**

* warn: If you try to add an instrument that has been added already.

**Returns:**

* None.

**Examples:**

```python
    # Add a new instrument to your algorithm
    alg = tng(name, regime, start_date, end_date)
    alg.addInstrument("btcusd")
```

## deleteInstrument

Deletes a specified instrument from an algorithm.

**Arguments:**

* ticker (str): Name of the instrument to delete.

**Returns:**

* None.

**Examples:**

```python
    # Adding two instruments and deleting one
    alg = tng(name, regime, start_date, end_date)
    alg.addInstrument("btcusd")
    alg.addInstrument("ethusd")
    alg.deleteInstrument("btcusd")
```

## addTimeframe

Adds specified timeframes to an algorithm.

**Arguments:**

* timeframes (tuple): Tuple of ints.

**Raises:**

* TypeError: If tuple has a non-int element.

**Returns:**

* None.

**Examples:**

```python
    # Adding a new instrument and 5- and 15-minute timeframes
    alg = tng(name, regime, start_date, end_date)
    alg.addInstrument("btcusd")
    alg.addTimeframe("btcusd", 5, 15)
```

## deleteTimeframe

Deletes specified timeframes from an algorithm.

**Arguments:**

* timeframes (tuple): Tuple of ints.

**Raises:**

* TypeError: If tuple has non-int element.

**Returns:**

* None.

**Examples:**

```python
    # Adding a new instrument and 15-minute timeframe
    alg = tng(name, regime, start_date, end_date)
    alg.addInstrument("btcusd")
    alg.addTimeframe("btcusd", 5, 15)
    alg.deleteTimeframe("btcusd", 5)
```
