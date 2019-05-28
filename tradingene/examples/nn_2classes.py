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


num_features = lookback = 5
lookforward = 1 
num_classes = 2 
num_epochs = 200
timeframe = 60  
ticker = "btcusd"
start_train_date = datetime(2017, 6, 1)
end_train_date = datetime(2017, 7, 1)
end_test_date = datetime(2017, 7, 6)

alg = None  # An instance of the "TNG" class used for simulated trading


def prepare_model():
    data = import_data(
        ticker,
        timeframe,
        start_train_date,
        end_train_date,
        calculate_input,
        lookback,
        calculate_output,
        lookforward,
        split=(100, 0, 0)
    )

    # Creating a model...
    model = Sequential()
    model.add(Dense(
            units=num_features * 2,
            activation='tanh',
            input_dim=num_features,
            kernel_initializer=he_uniform(1)))
    model.add(Dense(num_features * 2, activation='tanh'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
    one_hot_train_outputs = keras.utils.to_categorical(
        data['train_output'],
        num_classes=num_classes)  # Performing one-hot encoding
    model.fit(
        data['train_input'], one_hot_train_outputs,
        epochs=num_epochs)  # Training the model
    return model
# end of load_data


def calculate_input(data):
    input_vec = np.zeros(num_features)  # A vector to store inputs
    for i in range(lookback):
        input_vec[i] = np.log(data['open'][i] / data['close'][0])
    return np.array([input_vec])


def calculate_output(data):
    if data['close'][lookforward - 1] > data['open'][0]:
        return 1
    else:
        return 0


def onBar(instrument):
    inp = calculate_input(instrument.rates[1:lookback + 1])
    prediction = model.predict_classes(inp)[0]
    if prediction == 1:  # Class "1" predicts price to surge up...
        alg.buy()
    elif prediction == 0:  # Class "0" predicts price to fall down...
        alg.sell()


model = prepare_model()
alg = TNG(end_train_date, end_test_date)  # Creating an instance of TNG class to run algorithm within.
alg.addInstrument(ticker)  # Adding an instrument.
alg.addTimeframe(ticker, timeframe)  # Adding a time frame.
alg.run_backtest(onBar)  # Backtesting...

stat = bs.BacktestStatistics(alg)  # Retrieving statistics of the backtest

pnl = stat.calculate_PnL()  # Retrieving the PnL.
num_positions = stat.calculate_number_of_trades()  # Retrieving the number of trades done.
print("pnl=%f, num_positions=%d" % (pnl, num_positions))

stat.backtest_results()  # Displaying the backtest statistics
