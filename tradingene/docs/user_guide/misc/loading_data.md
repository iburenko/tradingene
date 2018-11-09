# Overview

Data could be loaded in two different ways. The first one returns "raw"
data, i.e. OHLC, volume data, the values of specified technical indicators. These data
 are useful either for research purposes or preparing inputs for machine learning algorithms or other issues. The second method returns data already prepared for fitting machine learning algorithms. See detailed explanations
 below.

## import_data

Loads data for a given ```ticker``` and ```timeframe``` from ```start_date``` to ```end_date```.
After _each_ bar of a given period, ticker and timeframe ```calculate_input```
and ```calculate_output``` functions are called. The function ```calculate_input```
uses the last ```lookback + 1``` candles in order to calculate an input vector, ```calculate_output```
uses ```lookforward + 1``` candles to calculate the corresponding output. The resulting data
will be split in proportion given by ```split```.

**Arguments:**

* ticker (str): Name of the underlying asset.

* timeframe (int): Timeframe given in minutes.

* start_date (datetime.datetime): Requests data from this date.

* end_date (datetime.datetime): Requests data up to this date.

* calculate_input (callable, default:None): Function that calculates input vector after
                 every fully formed bar in the requested time period.

* lookback (int, default:None): Function ```calculate_input``` will be able
          to use ```lookback + 1``` candles to calculate input vector.

* calculate_output (callable, default:None): Function that calculates output vector after
                  every fully formed bar in the requested time period.

* lookforward (int, default:None): Function ```calculate_output``` will be able
          to use ```lookforward + 1``` candles to calculate output.

* reverse (bool, default:True): If ```reverse``` then the most recent candles have
         lower index, i.e. the last candle starts at ```start_date```.

* split (tuple, default:(50,25,25)): Specifies proportion to split prepared data.
       All elements have to sum up to 100. The tuple ```split``` might be of
       length 2 or 3.

* indicators (dict, default:None): Dictionary of indicators that will be calculated
            and could be used in ```calculate_input``` or ```calculate_output```.
            Any key of the dictionary is a ```str``` value. The value of the dictionary must be a         tuple containing the name of the indicator and its parameters. A tuple with an indicator name only uses the default values.
            For instance:

```python
{'sma5':('sma', 5), 'sma10':('sma', 10, 'high'), 'rsi':('rsi'), 'stochastic3':('stochastic', 3)}
```

* cache (bool, default:True): If ```True```, calculated values will be stored locally.

* bootstrap (int, default:0): If 0 -- no bootsrap is used;
                              If 1 -- random sampling will be used to form input
                                    and output sets.

**Raises:**

* TypeError: If one of the arguments is not of the proper type.

* ValueError: If ```lookback``` or ```lookforward``` is less than 1.

**Returns:**

* dict:
    - if len(split) == 2:
      {'train_input': np.array(...), 'train_output': np.array(...),
      'test_input': np.array(...), 'test_output': np.array(...)}

    - if len(split) == 3:
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

Imports candles for a given ```ticker```, ```timeframe``` and time period.

**Arguments:**

* ticker (str): Name of the underlying asset.

* timeframe (int): Timeframe given in minutes.

* start_date (datetime.datetime): Requests data from this date.

* end_date (datetime.datetime): Requests data up to this date.

* reverse (bool, default:True): If ```reverse``` then the most recent candles have
         lower index, i.e. the last candle starts at ```start_date```.

* indicators (dict, default:None): Dictionary of indicators that will be calculated
           and could be used in ```calculate_input``` or ```calculate_output```.
           Any key of the dictionary is a ```str``` value. The value of the dictionary must be a         tuple containing the name of the indicator and its parameters. A tuple with an indicator name only uses the default values.
           For instance:

```python
{'sma5':('sma', 5), 'sma10':('sma', 10, 'high'), 'rsi':('rsi'), 'stochastic3':('stochastic', 3)}
```

* cache (bool, default:True): If ```True```, calculated values will be stored locally.

**Raises:**

* TypeError: If one of the arguments is not of the proper type.

**Returns:**

* DataFrame: Columns contain 'time', 'open', 'high', 'low', 'close', 'vol' and all indicators from ```indicators``` dictionary. If some of the indicators
           comprises several fields, DataFrame contains each.
