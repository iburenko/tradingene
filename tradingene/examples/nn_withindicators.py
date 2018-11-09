from datetime import datetime
from tradingene.data.load import import_data
from tradingene.algorithm_backtest.tng import TNG
import tradingene.backtest_statistics.backtest_statistics as bs
from keras.models import Sequential
from keras.layers import Dense
from keras.initializers import he_uniform
import keras
import numpy as np
import pandas as pd

LOOKBACK = 16  # How many prior candle bars each train sample embraces.
INDICATORS = {
    'sma2': ('sma', 2, 'close'),
    'sma4': ('sma', 4),
    'sma8': ('sma', 8),
    'sma16': ('sma', 16)
}  # Indicators to feed the NN with.
NUM_FEATURES = 4  # The number of features. This depends on how you implement the "calculate_input()" function.
LOOKFORWARD = 1  # How far in the future the algorithm "looks" and foresees.
NUM_CLASSES = 2  # The number of classes depends of what the "calculate_output()" fuction returns (see below)
NUM_EPOCHS = 100  # The number of epochs to train your model through.
TIMEFRAME = 60  # The time frame.
TICKER = "btcusd"  # The ticker.
START_TRAIN_DATE = datetime(2017, 5, 1)  # When a train period starts...
END_TRAIN_DATE = datetime(
    2017, 6, 1)  # When the train period ends and the test starts...
END_TEST_DATE = datetime(2017, 6, 6)  # When the test ends...

alg = None  # An instance of the "TNG" class used for simulated trading
model = None  # An instance of the model to train and use


def prepare_model():

    data = import_data(
        TICKER,
        TIMEFRAME,
        START_TRAIN_DATE,
        END_TRAIN_DATE,
        calculate_input,
        LOOKBACK,
        calculate_output,
        LOOKFORWARD,
        split=(
            100, 0, 0
        ),  # This time we need only a train set (100% for train set, 0% for test and validation ones)
        indicators=INDICATORS)

    # Creating a model...
    m = Sequential()  # Creating a model class instance
    # The number of nodes in the first hidden layer equals the number of features multiplied by 2
    m.add(
        Dense(
            units=NUM_FEATURES * 2,
            activation='tanh',
            input_dim=NUM_FEATURES,
            kernel_initializer=he_uniform(1)))
    # Adding another hidden layer
    m.add(Dense(NUM_FEATURES * 2, activation='tanh'))
    # Adding an output layer
    m.add(Dense(NUM_CLASSES, activation='softmax'))
    # Compiling the model
    m.compile(
        loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

    one_hot_train_outputs = keras.utils.to_categorical(
        data['train_output'],
        num_classes=NUM_CLASSES)  # Performing one-hot encoding
    m.fit(
        data['train_input'], one_hot_train_outputs,
        epochs=NUM_EPOCHS)  # Training the model
    return m


# end of load_data


def calculate_input(data):
    input_vec = np.zeros(NUM_FEATURES)  # A vector to store inputs
    input_vec[0] = np.log(data['sma2'][0] / data['close'][0])
    input_vec[1] = np.log(data['sma4'][0] / data['close'][0])
    input_vec[2] = np.log(data['sma8'][0] / data['close'][0])
    input_vec[3] = np.log(data['sma16'][0] / data['close'][0])
    return np.array([input_vec])


def calculate_output(data):
    if data['close'][LOOKFORWARD - 1] > data['open'][0]:
        return 1
    else:
        return 0


def onBar(instrument):
    # Converting rates into Pandas dataframe to attach indicators values next.
    rates = pd.DataFrame(instrument.rates[1:2])

    # Attaching sma(2), sma(4), sma(8) and sma(16) values to the 1st element of the "rates" array
    rates['sma2'] = [instrument.sma(2)[1]]
    rates['sma4'] = [instrument.sma(4)[1]]
    rates['sma8'] = [instrument.sma(8)[1]]
    rates['sma16'] = [instrument.sma(16)[1]]

    inp = calculate_input(
        rates)  # Passing rates and indicators values into "calculate_input"
    prediction = model.predict_classes(inp)[0]
    tpsl = instrument.rates['open'][0] * 0.005  # To set 0,5% take-profit and stop-loss
    if prediction == 1:  # Class "1" predicts price to surge up
        alg.buy()
        alg.setTP(tpsl)
        alg.setSL(tpsl)

    elif prediction == 0:  # Class "0" predicts price to fall down
        alg.sell()
        alg.setTP(tpsl)
        alg.setSL(tpsl)


model = prepare_model()  # Creating an ML-model.
alg = TNG(
    END_TRAIN_DATE,
    END_TEST_DATE)  # Creating an instance of environment to run algorithm in.
alg.addInstrument(TICKER)  # Adding an instrument.
alg.addTimeframe(TICKER, TIMEFRAME)  # Adding a time frame.
alg.run_backtest(onBar)  # Backtesting...

stat = bs.BacktestStatistics(alg)  # Retrieving statistics of the backtest

pnl = stat.calculate_PnL()
num_positions = stat.calculate_number_of_trades()
print("pnl=%f, num_positions=%d" % (pnl, num_positions))

stat.backtest_results()  # Displaying the backtest statistics
