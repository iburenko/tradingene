## Using SVM

With the Tradingene framework you are allowed to use all variety of machine learning methods, not restricting yourself with neural networks only. Two most popular libraries ```sklearn``` and ```keras``` are fully available for use as in the Framework so in the Platform.   

A sample script presented below implements a simple trading robot that makes trades according to the signals of an ```SVC``` model. To utilize such a model we import the required library first:

```python
from sklearn.svm import SVC
```

Next a model must be created and trained:
```python
# Creating an SVC model
model = SVC( tol=1e-5, degree=5 )

# Reshaping the inputs to be passed into the "fit" function
train_output = np.reshape(data['train_output'], (np.shape(data['train_output'])[0],) )

# Training the model
model.fit(data['train_input'], train_output)
```

Eventually when implementing the ```onBar()``` function we use the ```predict``` method of the ```SVC``` class just like we do with neural networks:
```python
prognosis = model.predict( [inp] )[0]
```

The whole script runs as follows:

```python
from datetime import datetime
from tradingene.data.load import import_data
from tradingene.algorithm_backtest.tng import TNG
import tradingene.backtest_statistics.backtest_statistics as bs
from sklearn.svm import SVC
import numpy as np

lookback = 3 # How many prior candle bars each train sample embraces.
num_features = _lookback # The number of features. This depends on how you implement the "calculate_input()" function.
    # This time the number of features equals the "lookback" period.   
lookforward = 1 # How far in the future the algorithm "looks" and foresees.
timeframe = 60 # The time frame.
ticker = "btcusd" # The ticker.
start_train_date = datetime(2018, 2, 5) # When a train period starts...
end_train_date = datetime(2018, 3, 5) # When the train period ends and the test starts...
end_test_date = datetime(2018, 3, 15) # When the test ends...

alg = None # An instance of the "TNG" class used for simulated trading

def prepare_model():
    data = import_data(
        ticker, timeframe, start_train_date, end_train_date,
        calculate_input, lookback, calculate_output, lookforward,
        split = (100, 0, 0) # This time we need only a train set (100% for train set, 0% for test and validation ones)
    )

    # Creating an SVC model
    model = SVC( tol=1e-5, degree=5 )

    # Reshaping the inputs to be passed into the "fit" function
    train_output = np.reshape(data['train_output'], (np.shape(data['train_output'])[0],) )

    # Training the model
    model.fit(data['train_input'], train_output)
    return model
# end of load_data


def calculate_input(data):
    input_vec = np.zeros(num_features) # A vector to store inputs
    for i in range(lookback):  
        input_vec[i] = 100.0 * (data['open'][i] - data['close'][0]) / data['close'][0]
    return input_vec


def calculate_output(data):
    if data['close'][lookforward-1] > data['open'][0]*1.01:
        return 1
    elif data['close'][lookforward-1]*1.01 < data['open'][0]:
        return -1
    else:
        return 0


def onBar(instrument):
    inp = calculate_input( instrument.rates[1:lookback+1] ) # Calculating inputs
    prognosis = model.predict([inp])[0] # Making prediction
    if prognosis > 0:
        alg.buy()
    elif prognosis < 0:
        alg.sell()
# end of onBar()


model = prepare_model() # Creating an ML-model.
alg = TNG(end_train_date, end_test_date) # Creating an instance of environment to run algorithm in.
alg.addInstrument(ticker) # Adding an instrument.
alg.addTimeframe(ticker, timeframe) # Adding a time frame.
alg.run_backtest(onBar) # Backtesting...

stat = bs.BacktestStatistics(alg) # Retrieving statistics of the backtest

pnl = stat.calculate_PnL() # Retrieving the PnL of the backtest.
num_positions = stat.calculate_number_of_trades() # Retrieving the number of trades made throughtout the backtest.
print("pnl=%f, num_positions=%d" % (pnl, num_positions) )

stat.backtest_results() # Displaying the backtest statistics
```
