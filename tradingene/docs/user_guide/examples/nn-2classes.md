### Classification with neural networks

Using neural networks for trading requires additional efforts in comparison with static, "no-learning" trading algorithms. First you have to prepare training data to learn a network with. To do this you use the ```import_data()``` function:
```python
    data = import_data(
        TICKER, TIMEFRAME, START_TRAIN_DATE, END_TRAIN_DATE,
        calculate_input, LOOKBACK, calculate_output, LOOKFORWARD,
        split = (100, 0, 0) # This time we need only a train set (100% for train set, 0% for test and validation ones)
   )
```
Please pay attention that along with a set of parameters two functions are passed into ```import_data()``` which are ```calculate_input``` and ```calculate_output```. You must implement these functions to calculate "inputs" and "outputs" you train your network with. For inputs we use price history in either form. This time we chose the following one:
```python
def calculate_input(data):
    input_vec = np.zeros(NUM_FEATURES) # A vector to store inputs
    for i in range(LOOKBACK):  
        input_vec[i] = np.log(data['open'][i] / data['close'][0])
    return np.array([input_vec])
```
To calculate network outputs we separate future returns into two classes: positive returns form class "1" while negative ones forms class"0":
```python
def calculate_output(data):
    if data['close'][LOOKFORWARD-1] > data['open'][0]:
        return 1
    else:
        return 0
```

Next you create a network. With the ```Keras``` library it may run as follows:

```python
    model = Sequential() # Creating a model class instance
    # The number of nodes in the first hidden layer equals the number of features multiplied by 2
    model.add(Dense(units=NUM_FEATURES*2, activation='tanh', input_dim=NUM_FEATURES, kernel_initializer=he_uniform(1)))
    # Adding another hidden layer
    model.add(Dense(NUM_FEATURES*2, activation='tanh'))
    # Adding an output layer
    model.add(Dense(NUM_CLASSES, activation='softmax'))
    # Compiling the model
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
```

After that you train your network with the data loaded:
```python
    model.fit(data['train_input'], one_hot_train_outputs, epochs=NUM_EPOCHS) # Training the model
```

Next you implement an ```onBar()``` function and code your trading logic in.
```python
def onBar(instrument):
    inp = calculate_input(instrument.rates[1:LOOKBACK+1]) # Calculating an input for the network
    prediction = model.predict_classes(inp)[0]           # MAking a prediction
    if prediction == 1: # Class "1" predicts price to surge up...
        alg.buy() # ...buying if so.
    elif prediction == 0: # Class "0" predicts price to fall down...
        alg.sell() # ...selling if so.
```

Eventually you may run a backtest to see how good or bad is the network in trading. As usual you do this with the following lines of code:
```python
alg = TNG(END_TRAIN_DATE, END_TEST_DATE) # Creating an instance of TNG class to run algorithm within.
alg.addInstrument(TICKER) # Adding an instrument.
alg.addTimeframe(TICKER, TIMEFRAME) # Adding a time frame.
alg.run_backtest(onBar) # Backtesting...
```

A sample script is presented below.

```python
from datetime import datetime
from tradingene.data.load import import_data
from tradingene.algorithm_backtest.tng import TNG
import tradingene.backtest_statistics.backtest_statistics as bs
from keras.models import Sequential
from keras.layers import Dense
from keras.initializers import he_normal, he_uniform
from keras.layers.normalization import BatchNormalization
import keras
import numpy as np

LOOKBACK = 5 # How many prior candle bars each train sample embraces.
NUM_FEATURES = LOOKBACK # The number of features. This depends on how you implement the "calculate_input()" function.
    # This time the number of features equals the "lookback" period.   
LOOKFORWARD = 1 # How far in the future the algorithm "looks" and foresees.
NUM_CLASSES = 2 # The number of classes depends of what the "calculate_output()" fuction returns (see below)
NUM_EPOCHS = 200 # The number of epochs to train your model through.
TIMEFRAME = 60 # The time frame.
TICKER = "btcusd" # The ticker.
START_TRAIN_DATE = datetime(2017, 6, 15) # When a train period starts...
END_TRAIN_DATE = datetime(2017, 7, 1) # When the train period ends and the test starts...
END_TEST_DATE = datetime(2017, 7, 6) # When the test ends...

alg = None # An instance of the "TNG" class used for simulated trading

def preparemodel():
    data = import_data(
        TICKER, TIMEFRAME, START_TRAIN_DATE, END_TRAIN_DATE,
        calculate_input, LOOKBACK, calculate_output, LOOKFORWARD,
        split = (100, 0, 0) # This time we need only a train set (100% for train set, 0% for test and validation ones)
   )

    # Creating a model...
    model = Sequential() # Creating a model class instance
    # The number of nodes in the first hidden layer equals the number of features multiplied by 2
    model.add(Dense(units=NUM_FEATURES*2, activation='tanh', input_dim=NUM_FEATURES, kernel_initializer=he_uniform(1)))
    # Adding another hidden layer
    model.add(Dense(NUM_FEATURES*2, activation='tanh'))
    # Adding an output layer
    model.add(Dense(NUM_CLASSES, activation='softmax'))
    # Compiling the model
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

    one_hot_train_outputs = keras.utils.to_categorical(data['train_output'], num_classes=NUM_CLASSES) # Performing one-hot encoding
    model.fit(data['train_input'], one_hot_train_outputs, epochs=NUM_EPOCHS) # Training the model
    return model
# end of load_data


def calculate_input(data):
    input_vec = np.zeros(NUM_FEATURES) # A vector to store inputs
    for i in range(LOOKBACK):  
        input_vec[i] = np.log(data['open'][i] / data['close'][0])
    return np.array([input_vec])


def calculate_output(data):
    if data['close'][LOOKFORWARD-1] > data['open'][0]:
        return 1
    else:
        return 0


def onBar(instrument):
    inp = calculate_input(instrument.rates[1:LOOKBACK+1]) # Calculating an input for the network
    prediction = model.predict_classes(inp)[0]           # MAking a prediction
    if prediction == 1: # Class "1" predicts price to surge up...
        alg.buy() # ...buying if so.
    elif prediction == 0: # Class "0" predicts price to fall down...
        alg.sell() # ...selling if so.


model = preparemodel() # Creating a network (an ML-model).
alg = TNG(END_TRAIN_DATE, END_TEST_DATE) # Creating an instance of TNG class to run algorithm within.
alg.addInstrument(TICKER) # Adding an instrument.
alg.addTimeframe(TICKER, TIMEFRAME) # Adding a time frame.
alg.run_backtest(onBar) # Backtesting...

stat = bs.BacktestStatistics(alg) # Retrieving statistics of the backtest

pnl = stat.calculate_PnL() # Retrieving the PnL.
num_positions = stat.calculate_number_of_trades() # Retrieving the number of trades done.
print("pnl=%f, num_positions=%d" % (pnl, num_positions))

stat.backtest_results() # Displaying the backtest statistics
```