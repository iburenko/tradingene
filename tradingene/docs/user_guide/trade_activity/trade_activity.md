# Overview

To implement your trading logic inside ```onBar``` function  you use the methods described in this section. Some of these methods duplicate others. Some methods might be replaced with several different ones. Some of the methods have been kept to provide backward compability (first of all with the [platform](https://www.tradingene.com)).

## openPosition()

### Usage

Opens a position without acquiring any asset.

**Arguments:**

* ticker (str, default:None): Asset for which position will be opened.

**Warns:**

* warn: If you are trying to open a new position but there is another one already opened. Only one opened position is allowed.

**Returns:**

* int: Random ```int``` if it is the first position while backtesting.

* int: Id of the last closed position increased by one if there has been at least one closed position.

* None: If position was not opened.

**Example:**

```python
# This example opens a position for btcusd.
alg = TNG(ticker, timeframe, start_date, end_date)
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 10)
alg.openPosition()
```
```python
# This example opens a position for btcusd.
alg = TNG(ticker, timeframe, start_date, end_date)
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 10)
alg.openPosition("btcusd")
```
---

## openLong()

### Usage

Opens a position and buys a specified number of lots.

This method combines functionality of the following two methods:

```python
alg.openPosition()
alg.buy(volume)
```
**Arguments:**

* volume (float, default:1.): Number of lots to buy.

**Warns:**

* warn: If there is an opened long position

**Returns:**

1. None: If the last position is opened and long;
2. pos_id (int): Position id returned by ```openPosition()```.

**Examples:**

```python
# In SP regime opens a position and buys 1 lot.
# Used volume is 1, available volume is 0.
def onBar(instrument):
  alg.openLong()
```
```python
# In SP regime opens a position and buys 1 lot.
# Used volume is 1, available volume is 0.
def onBar(instrument):
  alg.openLong(0.1)
```
```python
# In MP regime opens a position and buys 1 lot.
# Used volume is 1, available volume is 0.
def onBar(instrument):
  alg.openLong()
```
```python
# In MP regime opens a position and buys 0.1 lot.
# Used volume is 0.1, available volume is 0.9.
def onBar(instrument):
  alg.openLong(0.1)
```

---

## openShort()

### Usage

Opens a position and sells a specified number of lots.

This function combines functionality of the following two methods:
```python
alg.openPosition()
alg.sell(volume)
```

**Arguments:**

* volume (float, default:1.): Number of lots to sell.

**Warns:**

* warn: If there is an opened short position.

**Returns:**

1. None: If the last position is opened and short.
2. pos_id (int): Position id returned by ```openPosition()```.

**Examples:**

```python
# In SP regime opens a position and sells 1 lot.
# Used volume is -1, available volume is 0.
def onBar(instrument):
  alg.openShort()
```
```python
# In SP regime opens a position and sells 1 lot.
# Used volume is -1, available volume is 0.
def onBar(instrument):
  alg.openShort(0.1)
```
```python
# In MP regime opens a position and sells 1 lot.
# Used volume is -1, available volume is 0.
def onBar(instrument):
  alg.openShort()
```
```python
# In MP regime opens a position and sells 0.1 lot.
# Used volume is -0.1, available volume is 0.9.
def onBar(instrument):
  alg.openShort(0.1)
```

---

## closePosition()

### Usage

Closes the last opened position.

**Arguments:**

* id (int, default:None): id of a position to close.

**Warns:**

* warn: If there is no opened position.
* warn: If the position with specified id has been closed already.

**Returns:**

* None

**Examples:**

```python
# Opens a long position. If the last opening price
# was greater than 10000 closes this position.
def onBar(instrument):
  alg.openLong(1)
  if instrument.open[1] > 10000:
    alg.closePosition()
```

---

## onPositionClose()

### Usage

Calls the handler function right after position is closed.

Invokes handler function when the position referred by ```pos_id``` is closed.

**Arguments:**

* pos_id (int): id of a position.
* handler (callable): function to be invoked after position is closed.

**Raises:**

* ValueError: If the position referred by ```pos_id``` was not found.

* TypeError: If the handler is not callable.

**Returns:**

* None

**Examples:**

```python
# Works in any regime.
pos_id = None
def onBar(instrument):
  global pos_id
  pos_id = alg.openLong()
  alg.onPositionClose(pos_id, handler)
  alg.closePosition(pos_id)

def handler():
  print("Position closed!")
```

---

## buy()

### Usage
Buys a specified volume of an asset.

* In Single Position regime:
> buys 1 lot despite of the volume specified. If the last position is
closed then a new position will be opened automatically. If the last position is opened
and short then it will be closed and a new 1-lot long position will be opened. If the last position is opened and long then nothing will happen.

* In Multiple Position regime:
> buys a specified number of lots. If the last position is closed then a new position will be
opened. If the last trade in the position is short then the position won't be
closed but a specified number of lots will be bought. If the last trade
in the position is long then a specified number of lots will be bought.
Notice that volume of any position is limited as follows:
\- MAX_AVAILABLE_VOLUME <= used_volume <= MAX_AVAILABLE_VOLUME.

**Arguments**:

* volume (float, default:1.): Number of lots to buy.

**Warns**:

* warn: If the specified volume is negative.
* warn: If the last position is opened and long (in SP regime only).

**Raises**:

* ValueError: If the specified volume exceeds MAX_AVAILABLE_VOLUME (in SP regime only).
* ValueError: If cumulative volume of all trades within a position exceeds MAX_AVAILABLE_VOLUME (in MP regime only).

**Returns**:

* None

**Examples:**

```python
# In SP regime opens a position and buys 1 lot.
# Used volume is 1, available volume is 0.
def onBar(instrument):
  alg.openPosition()
  alg.buy()
```
```python
# In SP regime opens a position and buys 1 lot.
# Used volume is 1, available volume is 0.
def onBar(instrument):
  alg.openPosition()
  alg.buy(0.1)
```
```python
# In SP regime buys 1 lot.
# Position will be opened automatically.
# Used volume is 1, available volume is 0.
def onBar(instrument):
  alg.buy()
```
```python
# In SP regime buys 1 lot using buy()
# then closes opened long position
# and sells 1 lot using sell().
def onBar(instrument):
  alg.buy() # used volume is 1, available is 0;
  alg.sell() # used volume is -1, available volume is 0.
```
```python
# In MP regime buys 0.1 lots then buys 0.2 lots
def onBar(instrument):
  alg.buy(0.1) # used volume is 0.1, available is 0.9;
  alg.buy(0.2) # used volume is 0.3, available volume is 0.7.
```
```python
# In MP regime buys 0.1 lots then sells 0.2 lots
def onBar(instrument):
  alg.buy(0.1) # used volume is 0.1, available is 0.9;
  alg.sell(0.2) # used volume is -0.1, available volume is 0.9.
```

---

## sell()

### Usage

Sells a specified volume of an asset.

* In Single Position regime:
> sells 1 lot despite of the volume specified. If the last position is
closed then a new position will be opened automatically. If the last position is opened
and long then it will be closed and a new 1-lot short position will be opened. If the last position is opened and short then nothing will happen.

* In Multiple Position regime:
> sells a specified number of lots. If the last position is closed then a new position will be
opened. If the last trade in the position is long then the position won't be
closed but a specified number of lots will be sold. If the last trade
in the position is short then a specified number of lots will be sold.
Notice that volume of any position is limited as follows:
\- MAX_AVAILABLE_VOLUME <= used_volume <= MAX_AVAILABLE_VOLUME.

**Arguments:**

* volume (float, default:1.): Number of lots to sell.

**Warns:**

* warn: If the specified volume is negative.
* warn: If the last position is open and short (in SP regime only).

**Raises:**

1. ValueError: If the specified volume exceeds MAX_AVAILABLE_VOLUME (in SP regime only).
2. ValueError: If cumulative volume of positions exceeds MAX_AVAILABLE_VOLUME (in MP regime only).

**Returns:**

* None

**Examples:**

```python
# In SP regime opens a position and sells 1 lot.
# Used volume is -1, available volume is 0.
def onBar(instrument):
  alg.openPosition()
  alg.sell()
```
```python
# In SP regime opens a position and sells 1 lot.
# Used volume is -1, available volume is 0.
def onBar(instrument):
  alg.openPosition()
  alg.sell(0.1)
```
```python
# In SP regime sells 1 lot.
# Position will be opened automatically.
# Used volume is -1, available volume is 0.
def onBar(instrument):
  alg.sell()
```
```python
# In SP regime sells 1 lot using sell()
# then closes opened short position
# and buys 1 lot using buy().
def onBar(instrument):
  alg.sell() # used volume is -1, available is 0;
  alg.buy() # used volume is 1, available volume is 0.
```
```python
# In MP regime sells 0.1 lots then sells 0.2 lots
def onBar(instrument):
  alg.sell(0.1) # used volume is -0.1, available is 0.9;
  alg.sell(0.2) # used volume is -0.3, available volume is 0.7.
```
```python
# In MP regime sells 0.1 lots then buys 0.2 lots
def onBar(instrument):
  alg.sell(0.1) # used volume is -0.1, available is 0.9;
  alg.buy(0.2) # used volume is 0.1, available volume is 0.9.
```

---

## setSL()

### Usage

Sets the maximum loss for a position.

After a position is opened a user is able to define the maximum acceptable loss.
While backtesting the current profit of the position is checked at every tick.
If the loss becomes greater than the specified value then the position
will be closed automatically.

If you wish to cancel ```stoploss```, set the stop-loss to zero.

**Arguments:**

* loss (float, default:None): Value of the stop-loss.

**Raises:**

* ValueError: If loss is not nonnegative.

**Returns:**

* None

**Examples:**

```python
# Works in any regime.
def onBar(instrument):
  alg.buy()
  alg.setSL(loss = 300)
  alg.setSL(loss = 0)
```

---

## setTP()

### Usage

Sets the maximum profit for a position.

After a position is opened a user is able to define the minimum desired profit.
While backtesting the current profit of the position is checked at every tick.
If the profit becomes greater than the specified value then the position
will be closed automatically.

If you wish to cancel ```takeprofit```, set the stop-loss to zero.

**Arguments:**

* profit (float, default:None): Value of the take-profit.

**Raises:**

* ValueError: If profit is not nonnegative.

**Returns:**

* None

**Examples:**

```python
# Works in any regime.
def onBar(instrument):
  alg.buy()
  alg.setTP(profit = 300)
  alg.setTP(profit = 0) #Cancels take-profit.
```

---

## setSLTP()

### Usage

Sets the stop-loss and take-profit.

Invoke of this function is equivalent to the following code:
```python
alg.setSL(loss)
alg.setTP(profit)
```

**Arguments:**

* loss (float, default:None): Value of the stop-loss.
* profit (float, default:None): Value of the take-profit.

**Returns:**

* None

**Examples:**

```python
# Sets the stop-loss and take-profit with a single method.
# Works in any regime.
def onBar(instrument):
  alg.buy()
  alg.setSLTP(loss = 300, profit = 300)
  # equivalelnt to
  alg.setSL(loss = 300)
  alg.setTP(profit = 300)
```

---

## getAvailableVolume()

### Usage

Returns the volume available for trading.

If the last position is opened calculates available volume. Notice that for the available volume the following inequality holds:

> 0 <= available volume <= MAX_AVAILABLE_VOLUME.

**Warns:**

* warn: If the last position is closed.

**Returns:**

* None: If the last position is not opened
* float: If the last position is opened.

**Examples:**

```python
# In SP regime
def onBar(instrument):
  alg.buy()
  alg.getAvailableVolume() # returns 0
```
```python
# In MP regime
def onBar(instrument):
  alg.buy(0.2)
  alg.getAvailableVolume() # returns 0.8
```
```python
# In MP regime
def onBar(instrument):
  alg.sell(0.5)
  alg.getAvailableVolume() # returns 0.5
```

---

## getLastPrice()

### Usage

Returns the last price simulated while backtesting.

Returns the last price for a specified instrument. If the instrument
is not specified then the last price of the first-added
instrument will be returned.

**Arguments:**

* ticker (str, default:None): Name of the underlying asset.

**Returns:**

* float: Last price simulated while backtesting.

**Raises:**

* AssertionError: If only one instrument has been added by a user, and a non-exisiting ticker was specified.
* NameError: If the ticker was not found among the added instruments.

**Examples:**

```python
# Works in any regime.
alg = TNG(name, regime, start_date, end_date)
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 10)
def onBar(instrument):
  alg.getLastPrice()
```
```python
# Works in any regime.
alg = TNG(name, regime, start_date, end_date)
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 10)
def onBar(instrument):
  alg.getLastPrice("btcusd")
```
```python
# Works in any regime.
alg = TNG(name, regime, start_date, end_date)
alg.addInstrument("btcusd")
alg.addInstrument("ethbtc")
alg.addTimeframe("btcusd", 10)
alg.addTimeframe("ethbtc", 15, 30)
def onBar(instrument):
  # Returns the last price of btcusd
  alg.getLastPrice()
```
```python
# Works in any regime.
alg = TNG(name, regime, start_date, end_date)
alg.addInstrument("btcusd")
alg.addInstrument("ethbtc")
alg.addTimeframe("btcusd", 10)
alg.addTimeframe("ethbtc", 15, 30)
def onBar(instrument):
  alg.getLastPrice()# Returns the last price of btcusd
  alg.getLastPrice("ethbtc")
```

---

## getPositionSide()

### Usage

Returns a position side given position's id ```pos_id```.

**Arguments:**

* pos_id (int): Id of the position

**Raises:**

* TypeError: If ```pos_id``` is not integer

* ValueError: If a position with ```pos_id``` was not found

**Returns:**

* float:
  * +1., if a position was long;
  * -1., if a position was short

**Examples:**

```python
# Works in both regimes
def onBar(instrument):
  pos_id = alg.buy()
  pos_side = alg.getPositionSide(pos_id)
  # pos_side equals 1.
```

---

## on()

### Usage

Waits for a specified event and calls the handler.

User can specify two types of events: Price event and Time event.

- Price event:
    Waits for a specified price. At the moment the current price
    strikes the specified price the handler will be called.
- Time event:
    Waits for a specified time. At the moment the current time
    is equal to or exceeds the specified time the handler will be called.

Can be cancelled with [off()](#off) call.

**Arguments:**

* type_ (str, default:None): Name of the type of event: "Price" or "Time".
* params (default:None): For Price event -- price (float).
                       For Time event -- time (int).
* argument (tuple, default:None): Arguments for a handler method.
* handler (function, default:None): method to be invoked when the specified event happens.

**Returns:**

* int: id of the event.

**Raises:**

* ValueError: If type_ was neither "Price" nor "Time".

**Examples:**

```python
# Works in any regime.
event_id = None
def onBar(instrument):
  global event_id
  event_id = alg.on("Price", 10000, handler)

def handler():
  print("Price event handler!")
```
```python
# Works in any regime.
event_id = None
def onBar(instrument):
  global event_id
  event_id = alg.on("Time", 20180201000000, handler)

def handler():
  print("Time event handler!")
```

---

## off()

### Usage

Cancels event.

If an event was set by [on()](#on) method, [off()](#off) will cancel it.

**Arguments:**

* id (int): id of the event.

**Returns:**

* None

**Warns:**

* warn: If no event with the specified id was found.

**Examples:**

```python
# Works in any regime.
event_id = None
def onBar(instrument):
  global event_id
  event_id = alg.on("Price", 10000, handler)
  if alg.getLastPrice() > 10000:
    alg.off(event_id)

def handler():
  global event_id
  print("Price event handler!")
```
```python
# Works in any regime.
event_id = None
def onBar(instrument):
  global event_id
  event_id = alg.on("Time", 20180201000000, handler)
  if instrument.time > 20180201000000:
    alg.off(event_id)

def handler():
  print("Time event handler!")
```
