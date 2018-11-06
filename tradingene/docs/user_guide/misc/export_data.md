# Overview

If one wants to analyze backtest results of an algorithm it is possible via ```export_results``` method. This method exports in a specified csv-file user requested data.

## export_data()

    export_data(indicators, lookback, filename=None)

For every closed position ```export_data``` exports data from the preceding ```lookback+1``` candles. Data comprises

* Time when position was closed;
* Close price;
* Position's side;
* Profit;
* Indicators values.

If ```filename``` is not specified saves data into the file ```results.csv``` otherwise saves data into the file with given name.


**Arguments:**

    indicators (dict): Dictionary of indicators of the form
               {indname1:(indparams1), indname2:(indparams2), ...}

    lookback (int): Store lookback+1 candles

    filename (str, default:None): Name of destionation file.
              If filename is None data will be exported to results.csv

**Raises:**

    TypeError: if one of arguments is not of the proper type

**Returns:**

    None
