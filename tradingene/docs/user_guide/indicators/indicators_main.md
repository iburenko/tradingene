Here we list all indicators that available in ```onBar``` method.

### ADX

Calculates values of the ADX indicator.

**Arguments**:

* periodADX (optional, default:14): is the ADX smoothing period,

* periodDI (optional, default:14): is the "+DI" and "-DI" smoothing period,

* priceType (optional, default:"close"): is one of the following: "open", "high", "low", "close"

**Returns**:

* An instance of the ```IndVals``` class with the following attributes:
    * adx (list, np.float64): A list of "adx" values of the indicator.
    * pdi (list, np.float64): The "+DI" line values.
    * mdi (list, np.float64): The "-DI" line values.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the values of ADX for the latest fully formed candle:
    valueOfADX = instrument.adx(periodADX=10).adx[1]        
    plusDI = instrument.adx(periodADX=10).pdi[1]        
    minusDI = instrument.adx(period=10).mdi[1]        
    # Please note that the "periodADX" argument is specified explicitly
    # while the other ones receives the default values.
```

### APO

Calculates values of the "APO" indicator.

**Arguments**:

* periodFast (optional, default:12): the period of the "fast" smoothing moving average.
* periodDI (optional, default:26): the period of the "slow" smoothing moving average.
* priceType (optional, default:"close"): is one of the following: "open", "high", "low", "close".

**Returns**:

* list (np.float64): A list of values of the "APO" indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    value = instrument.apo( periodFast=10 )[1]
    # Please note that the "periodFast" argument is specified explicitly while for
    # the other arguments the default values are used.  
```


### AROON

Calculates values of the AROON indicator.

**Arguments**:

* period (optional, default:25) is the period of "Aroon",
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close"


**Returns**:

* An instance of the ```IndVals``` class with the following attributes:
    * up (list, np.float64): A list of "Aroon Up" values.
    * down (list, np.float64): A list of "Aroon Down" values.


See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the values of ADX for the latest fully formed candle:
    aroonUp = instrument.aroon(period=10).up[1]        
    aroonDown = instrument.aroon(period=10).down[1]        
    # Please note that the "period" argument is specified explicitly
    # while the "priceType" one receives the default value "close".
```

### ATR

Calculates values of the "ATR" indicator.

**Arguments**:

* period (optional, default:14) is the period of the indicator,
* maType (optional, default:"sma") is the type of moving average to use (the possible values are: "sma", "ema", "wma", rma")


**Returns**:

* list (np.float64): A list of values of the "ATR" indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of ATR for the latest fully formed candle.
    value = instrument.atr( period=10 )[1]
    # Please note that the "period" argument is specified explicitly while
    # for "maType" the default value is used.  
```


### BOLLINGER

Calculates values of the BOLLINGER indicator.

**Arguments**:

* period (optional, default:20) is the period of the indicator,
* shift (optional, default:2.0) is width of the bands measured in standard deviations,
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close"


**Returns**:

* An instance of the ```IndVals``` class with the following attributes:
    * ma (list, np.float64): A list of the "middle" line values.
    * top (list, np.float64): The "top" line values.
    * bottom (list, np.float64): The "bottom" line values.


See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the values of BOLLINGER for the latest fully formed candle:
    ma = instrument.bollinger(period=10).ma[1]        
    top = instrument.bollinger(period=10).top[1]        
    bottom = instrument.adx(period=10).bottom[1]        
    # Please note that the "period" argument is specified explicitly
    # while the other ones receive the default values.
```

### CCI

Calculates values of the "CCI" indicator.

**Arguments**:

* period (optional, default:20) is the period of the indicator,
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* list (np.float64): A list of values of the "CCI" indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    value = instrument.cci( period=10 )[1]
    # Please note that the "period" argument is specified explicitly while for
    # the other one the default value is used.  
```


### CHANDE

Calculates values of the "CHANDE MOMENTUM" indicator.

**Arguments**:

* period (optional, default:10) is the period of "Chande Momentum".
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* list (np.float64): A list of values of the "APO" indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    value = instrument.chande( period=10 )[1]
    # Please note that the "period" argument is specified explicitly while for
    # the other one the default value is used.  
```


### EMA

Calculates values of the Exponential Moving Average (EMA) indicator.

**Arguments**:

* period (optional, default:9) is the period of the indicator.
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* list (np.float64): A list of values of the "EMA" indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    valueOfEMA = instrument.ema( period=10 )[1]
    # Please note that the "period" argument is specified explicitly while for
    # the other one the default value is used.  
```

### KELTNER

Calculates values of the KELTNER CHANNELS indicator.

**Arguments**:

* period (optional, default:20) is the period of the indicator,
* shift (optional, default:2.0) is width of the bands measured in standard deviations,
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* An instance of the ```IndVals``` class with the following attributes:
    * basis (list, np.float64): A list of the "basis" line values.
    * upper (list, np.float64): The "upper" line values.
    * lower (list, np.float64): The "lower" line values.


See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the values of KELTNER CHANNELS for the latest fully formed candle:
    basis = instrument.keltner(period=10).basis[1]        
    upper = instrument.keltner(period=10).upper[1]        
    lower = instrument.keltner(period=10).lower[1]        
    # Please note that the "period" argument is specified explicitly
    # while the other ones receive the default values.
```

### MACD

Calculates values of the Moving Average Convergence-Divergence (MACD) indicator.

**Arguments**:

* periodFast (optional, default:12) is the period the fast line of MACD.
* periodSlow (optional, default:26) is the period the slow line of MACD.
* periodSignal (optional, default:9) is the period the signal line of MACD.
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* An instance of the ```IndVals``` class with the following attributes:
    * macd (list, np.float64): A list of the MACD values.
    * signal (list, np.float64): The MACD Signal line values.
    * histogram (list, np.float64): The MACD histogram values.


See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the values of KELTNER CHANNELS for the latest fully formed candle:
    macd = instrument.macd(periodFast=10).macd[1]        
    signal = instrument.signal(periodFast=10).signal[1]        
    histogram = instrument.histogram(periodFast=10).histogram[1]        
    # Please note that the "periodFast" argument is specified explicitly
    # while the other ones receive the default values.
```

### MOMENTUM

Calculates values of the MOMENTUM indicator.

**Arguments**:

* period (optional, default:10) is the period of the indicator.
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* list (np.float64): A list of values of the MOMENTUM indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    value = instrument.momentum( period=10 )[1]
    # Please note that the "period" argument is specified explicitly while for
    # the other argument the default value is used.  
```

### PPO

Calculates values of the PPO indicator.

**Arguments**:

* periodFast (optional, default:12) is the period of the fast moving average.
* periodSlow (optional, default:26) is the period of the slow moving average.
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* list (np.float64): A list of values of the PPO indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    value = instrument.ppo( periodFast=10 )[1]
    # Please note that the "periodFast" argument is specified explicitly while for
    # the other arguments the default values are used.  
```

### ROC

Calculates values of the ROC indicator.

**Arguments**:

* period (optional, default:9) is the period of the indicator.
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* list (np.float64): A list of values of the ROC indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    value = instrument.roc( period=12 )[1]
    # Please note that the "period" argument is specified explicitly while for
    # the other argument the default value is used.  
```

### RSI

Calculates values of the Relative Strength Index (RSI) indicator.

**Arguments**:

* period (optional, default:14) is the period of the indicator.
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* list (np.float64): A list of values of the RSI indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    value = instrument.rsi( period=12 )[1]
    # Please note that the "period" argument is specified explicitly while for
    # the "priceType" argument the default value is used.  
```

### SMA

Calculates values of the Simple Moving Average (SMA) indicator.

**Arguments**:

* period (optional, default:9) is the period of the indicator.
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* list (np.float64): A list of values of the "SMA" indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    valueOfSMA = instrument.sma( period=10 )[1]
    # Please note that the "period" argument is specified explicitly while for
    # the other one the default value is used.  
```

### STOCHASTIC

Calculates values of Stochastic Oscillator.

**Arguments**:

* period (optional, default:14) is the period of the oscillator to calculate the 'K' line.
* periodD (optional, default:3) is the smoothing period to calculate the 'D' line.
* smoothing (optional, default:1) is the initial smoothing for the 'K' line.


**Returns**:

* An instance of the ```IndVals``` class with the following attributes:
    * d (list, np.float64): A list of "d" values of the indicator.
    * k (list, np.float64): A list of "k" values of the indicator.


See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the values of STOCHASTIC for the latest fully formed candle:
    valueOfK = instrument.stochastic(period=10, periodD=4).k[1]        
    valueOfD = instrument.stochastic(period=7, periodD=5).d[1]        
    # Please note that the "period" and "periodD" arguments are specified explicitly
    # while the "smoothing" argument receives default value "1".
```

### TRIMA

Calculates values of the TRIPPLE MOVING AVERAGE (TRIMA) indicator.

**Arguments**:

* period (optional, default:10) is the period of the indicator.
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* list (np.float64): A list of values of the TRIMA indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    valueOfTRIMA = instrument.trima( period=10 )[1]
    # Please note that the "period" argument is specified explicitly while for
    # the "priceType" the default value is used.  
```

### WILLIAMS

Calculates values of the TRIPPLE MOVING AVERAGE (TRIMA) indicator.

**Arguments**:

* period (optional, default:10) is the period of the indicator.
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* list (np.float64): A list of values of the TRIMA indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    valueOfTRIMA = instrument.trima( period=10 )[1]
    # Please note that the "period" argument is specified explicitly while for
    # the "priceType" the default value is used.  
```

### WMA

Calculates values of the Weighted Moving Average (WMA) indicator.

**Arguments**:

* period (optional, default:9) is the period of the indicator.
* priceType (optional, default:"close") is one of the following: "open", "high", "low", "close".


**Returns**:

* list (np.float64): A list of values of the "WMA" indicator.

See also: [How to Address Indicator Values](how_to_address_indicator_values.md).

**Examples:**

```python
def onBar(instrument):
    # Retrieving the value of APO for the latest fully formed candle.
    valueOfSMA = instrument.wma( period=10 )[1]
    # Please note that the "period" argument is specified explicitly while for
    # the other one the default value is used.  
```
