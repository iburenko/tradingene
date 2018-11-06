# Overview

Generally data could be loaded in two different ways. One of them returns "raw"
data, i.e. OHLC, volume data, values of specified technical indicators. These data
 are useful for either research purposes or preparing them as inputs for the
 machine learning algorithms or other issues. Another method returns already prepared
 data that could be used for fitting machine learning algorithms. See detailed explanations
 below.

## import_data

Loads data for given ```ticker``` and ```timeframe``` from ```start_date``` to ```end_date```.
In the given period, ticker and timeframe after _each_ bar ```calculate_input```
and ```calculate_output``` methods are called. The method ```calculate_input```
uses the last ```lookback + 1``` candles in order to calculate input vector, ```calculate_output```
uses ```lookforward + 1``` candles to calculate corresponding output. Resulting data
will be split in proportion given by ```split```.

**Arguments:**

* ticker (str): Name of the underlying asset.

* timeframe (int): Timeframe given in minutes.

* start_date (datetime.datetime): Request data from this date.

* end_date (datetime.datetime): Request data until this date.

* calculate_input (callable, default:None): Method that calculates input after
                 every fully formed bar in the requested time period.

* lookback (int, default:None): The method ```calculate_input``` will be able
          to use ```lookback + 1``` candles to calculate input vector.

* calculate_output (callable, default:None): Method that calculates output after
                  every fully formed bar in the requested time period.

* lookforward (int, default:None): The method ```calculate_output``` will be able
          to use ```lookforward + 1``` candles to calculate output.

* reverse (bool, default:True): If ```reverse``` then the most recent candles have
         lower index, i.e. the the last candle starts at ```start_date```.

* split (tuple, default:(50,25,25)): In which proportion split prepared data.
       All elements need to sum up to 100. The tuple ```split``` might be of
       length 2 or 3.

* indicators (dict, default:None): Dictionary of indicators that will be calculated
            and could used in ```calculate_input``` or ```calculate_output```.
            Key of the dictionary is the name of indicator, value must contain
            tuple of parameters, empty tuple is allowed. Empty tuple corresponds
            to values by default.
            For instance: ```{'sma':(10, 'high'), 'rsi':(), 'stochastic':(3)}```.

* cache (bool, default:True): If ```True``` calculated values will be stored locally.

* bootstrap (int, default:0): If 0 -- no bootsrap is used;
                              If 1 -- random sampling will be used to form input
                                    and output sets.

**Raises:**

    TypeError: If one of arguments is not of the proper type.

    ValueError: If ```lookback``` or ```lookforward``` is less than 1

**Returns:**

    dict:
        if len(split) == 2:
          {'train_input': np.array(...), 'train_output': np.array(...),
          'test_input': np.array(...), 'test_output': np.array(...)}

        if len(split) == 3:
          {'train_input': np.array(...), 'train_output': np.array(...),
          'test_input': np.array(...), 'test_output': np.array(...),
          'validation_input': np.array(), 'validation_output': np.array()} if len(split) == 3

        'train_input' (np.array): input data for the train dataset
        'train_output' (np.array): output data for the train dataset
        'test_input' (np.array): input data for the test dataset
        'test_output' (np.array): output data for the test dataset
        'validation_input' (np.array): input data for the validation dataset
        'validation_output' (np.array): output data for the validation dataset

## import_candles

Import candles

**Arguments:**

* ticker (str): Name of the underlying asset.

* timeframe (int): Timeframe given in minutes.

* start_date (datetime.datetime): Request data from this date.

* end_date (datetime.datetime): Request data until this date.

* reverse (bool, default:True): If ```reverse``` then the most recent candles have
         lower index, i.e. the the last candle starts at ```start_date```.

* indicators (dict, default:None): Dictionary of indicators that will be calculated
            and could used in ```calculate_input``` or ```calculate_output```.
            Key of the dictionary is the name of indicator, value must contain
            tuple of parameters, empty tuple is allowed. Empty tuple corresponds
            to values by default.
            For instance: ```{'ema':(5, 'low'), 'macd':(3), 'stochastic':()}```.

* cache (bool, default:None): If ```True``` calculated values will be stored locally.

**Raises:**

    TypeError: If one of arguments is not of the proper type.

**Returns:**

    DataFrame: Columns contains 'time', 'open', 'high', 'low', 'close', 'vol'
               and all indicators from ```indicators```. If some of indicators
               comprises several field DataFrame contains each.
