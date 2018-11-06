## How to address indicator values

Most indicators calculate only one value for each candle bar. If so the values are retrieved in the form of a list where index "1" refers to the latest fully formed candle, index "2" refers to the one preceeding it and so on. The number of values in the list can not exceed **50**. Before addressing a value in the list you are recommended to use the "**len()**" function to avoid "*index out of range*" error.

**Example:**
```python
    def onBar(instrument):
        # Retrieving the value of APO for the latest fully formed candle.
        value = instrument.apo(periodFast=10)[1]
        # Please note that the "periodFast" argument is specified explicitly while for
        # the other arguments the default values are used.  
```


if an indicator calculates more than one value for each candle bar, the values are retrieved as an instance of a special internal class (named "IndVals)" with each attribute refering to the corresponding list of values. Each list is indexed in the same way described above: index "1" refers to the latest fully formed candle, index "2" refers to the one preceeding it and so on. Before addressing a value in the list you are recommended to use the "**len()**" function to avoid "*index out of range*" error.

**Example:**
```python
    def onBar(instrument):
        # Retrieving the values of STOCHASTIC for the latest fully formed candle:
        valueOfK = instrument.stochastic(period=10, periodD=4).k[1]        
        valueOfD = instrument.stochastic(period=7, periodD=5).d[1]        
        # Please note that the "period" and "periodD" arguments are specified explicitly
        # while the "smoothing" argument receives default value "1".
```
