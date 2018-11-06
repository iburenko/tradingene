# Overview

Any algorithm needs an instance of the ```TNG``` class. This instance contains all the methods required for trading and backtesting. To create an instance of the ```TNG``` class you must specify the starting and ending dates of a backtest. You may explicitly specify the name of your algorithm and the backtest regime. If you do not specify these arguments the default values will be used.

## Name

about ```name```.

## Regime

about ```regime```.

**Arguments:**

    name (str, default: "Cornucopia"): Name of the algorithm;
    regime (str, default: "SP"): Controls the number of trades in a single position.
            In the "SP" regime only one trade is allowed, in the "MP" multiple trades are allowed.
    start_date (datetime.datetime): Starting time of the backtest.
    end_date (datetime.datetime): Ending time of the backtest.            

**Raises:**

* ValueError: If four variables were sent to the constructor but not
            in the following order: (name, regime, start_date, end_date).
* ValueError: If more than two string variables were sent to the constructor.

* ValueError: If ```regime``` is not "SP" or "MP".

* ValueError: If the constructor receives more that two string variables.

* ValueError: If the constructor receives anything different from
            two datetime variables.
* ValueError: If ```start_date``` is equal to ```end_date```.

**Examples:**
```python
# Constructor with only two parameters.
# default values for name and regime will be used.
# default name is "Cornucopia",
# default regime is "SP" (single position).
# Note: start_date and end_date may be specified
# in any order.
from datetime import datetime
from tradingene.algorithmic_backtest.tng import TNG
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 2, 1)
alg = TNG(start_date, end_date)
```

```python
# Constructor with three parameters:
# name, start_date, end_date;
# by default regime is "SP".
# Note: start_date and end_date may be specified
# in any order
from datetime import datetime
from tradingene.algorithmic_backtest.tng import TNG
name = "Fleece"
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 2, 1)
alg = TNG(name, start_date, end_date)
```

```python
# Constructor with three parameters:
# regime, start_date, end_date;
# by default name is "Cornucopia".
# Note: start_date and end_date may be specified
# in any order.
from datetime import datetime
from tradingene.algorithmic_backtest.tng import TNG
regime = "MP"
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 2, 1)
alg = TNG(name, start_date, end_date)
```

```python
# Constructor with four parametera:
# name, regime, start_date, end_date
# Note: name must be specified before regime,
# after name and regime start_date, end_date
# may be specified in any order.
name = "Fleece"
regime = "MP"
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 2, 1)
alg = TNG(name, regime, start_date, end_date)
```
