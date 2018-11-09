# Overview

If you wish to analyze backtest results of an algorithm it could be done with the ```export_results``` function. This function exports data requested by a user into a specified csv-file.

## export_data()

    export_data(indicators, lookback, filename=None)

For every closed position ```export_data``` exports data related to the preceding ```lookback+1``` candles. The data comprises

* Time the position was closed;
* Closing price;
* Position's side;
* Profit;
* Indicators values.

If ```filename``` is not specified the function saves the data into the file ```results.csv``` otherwise saves data into the file with a given name.


**Arguments:**

* indicators (dict): Dictionary of indicators of the form
           {indname1:(indname, indparams1), indname2:(indname, indparams2), ...}

* lookback (int): Specifies lookback period.

* filename (str, default:None): Name of the destination file.
          If "filename" is None the data will be exported to "results.csv".

**Raises:**

* TypeError: if one of the arguments is not of the proper type.

**Returns:**

* None
