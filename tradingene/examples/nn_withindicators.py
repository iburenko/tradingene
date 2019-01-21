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

lookback = 16  # How many prior candle bars each train sample embraces.
indicators = {
    'sma2': ('sma', 2, 'close'),
    'sma4': ('sma', 4),
    'sma8': ('sma', 8),
    'sma16': ('sma', 16)
}  # Indicators to feed the NN with.
num_features = 4  # The number of features. This depends on how you implement the "calculate_input()" function.
lookforward = 1  # How far in the future the algorithm "looks" and foresees.
num_classes = 2  # The number of classes depends of what the "calculate_output()" fuction returns (see below)
num_epochs = 100  
timeframe = 60  
ticker = "btcusd"
start_train_date = datetime(2017, 5, 1) 
end_train_date = datetime(
    2017, 6, 1)
end_test_date = datetime(2017, 6, 6) 

alg = None  # An instance of the "TNG" class used for simulated trading
model = None  # An instance of the model to train and use


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
        split=(100, 0, 0),
        indicators=indicators)

    m = Sequential()
    m.add(
        Dense(
            units=num_features * 2,
            activation='tanh',
            input_dim=num_features,
            kernel_initializer=he_uniform(1)))
    m.add(Dense(num_features * 2, activation='tanh'))
    m.add(Dense(num_classes, activation='softmax'))
    m.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
    one_hot_train_outputs = keras.utils.to_categorical(data['train_output'], num_classes=num_classes)
    m.fit(data['train_input'], one_hot_train_outputs, epochs=num_epochs)
    return m
# end of load_data


def calculate_input(data):
    input_vec = np.zeros(num_features)  # A vector to store inputs
    input_vec[0] = np.log(data['sma2'][0] / data['close'][0])
    input_vec[1] = np.log(data['sma4'][0] / data['close'][0])
    input_vec[2] = np.log(data['sma8'][0] / data['close'][0])
    input_vec[3] = np.log(data['sma16'][0] / data['close'][0])
    return np.array([input_vec])


def calculate_output(data):
    if data['close'][lookforward - 1] > data['open'][0]:
        return 1
    else:
        return 0


def onBar(instrument):
    rates = pd.DataFrame(instrument.rates[1:2])
    # Attaching sma(2), sma(4), sma(8) and sma(16) values to the 1st element of the "rates" array
    rates['sma2'] = [instrument.sma(2)[1]]
    rates['sma4'] = [instrument.sma(4)[1]]
    rates['sma8'] = [instrument.sma(8)[1]]
    rates['sma16'] = [instrument.sma(16)[1]]

    inp = calculate_input(rates)
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


model = prepare_model()
alg = TNG(end_train_date, end_test_date)
alg.addInstrument(ticker)  # Adding an instrument.
alg.addTimeframe(ticker, timeframe)  # Adding a time frame.
alg.run_backtest(onBar)  # Backtesting...

stat = bs.BacktestStatistics(alg)  # Retrieving statistics of the backtest

pnl = stat.calculate_PnL()
num_positions = stat.calculate_number_of_trades()
print("pnl=%f, num_positions=%d" % (pnl, num_positions))

stat.backtest_results()  # Displaying the backtest statistics
