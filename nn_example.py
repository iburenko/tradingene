from datetime import datetime
from time import time
from tng.data.load import import_data
from tng.algorithm_backtest.tng import TNG
import tng.backtest_statistics.backtest_statistics as bs
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.initializers import he_normal, he_uniform
from keras.layers.normalization import BatchNormalization
import keras
import numpy as np
import cProfile
import pstats


def train_model():
    start_date = datetime(2017, 6, 1)
    end_date = datetime(2018, 3, 1)
    ticker = "ethbtc"
    timeframe = 60
    lookback = 5
    lookforward = 2
    # inds = {'sma':(10, 'open'), 'ema':(3), 'rsi':(), 'apo':(), \
    #         'atr':(), 'cci':(), 'chande':(), \
    #         'momentum': (), 'ppo':(), 'roc':(), \
    #         'trima':(), 'williams':(),\
    #         'bollinger':(), 'macd':(), 'keltner':()}
    inds = {'sma':(), 'macd':()}
    data = import_data(
        ticker, timeframe, start_date, end_date, 
        calculate_input, lookback, 
        calculate_output, lookforward,
        split = (50, 30, 20), indicators = inds
    )
    model = create_model()
    outputs = keras.utils.to_categorical(data['train_output'], num_classes=3)
    model.fit(data['train_input'], outputs, epochs=10)
    val_outpus = keras.utils.to_categorical(data['validation_output'], num_classes = 3)
    loss, acc = model.evaluate(data['validation_input'], val_outpus)
    return model

def create_model():
    model = Sequential()
    model.add(Dense(units=100, activation='tanh', input_dim=10, kernel_initializer=he_uniform(1)))
    model.add(Dense(100, activation='tanh'))
    model.add(Dense(3, activation='softmax'))
    model.compile(
        loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
    return model


def calculate_input(data):
    # print(list(map(int,(data.time))))
    # input("")
    input_vec = np.zeros(10)
    open_prices = data['open']
    volumes = data['vol']
    for i in range(5):
        input_vec[i] = open_prices[i]
        input_vec[i + 5] = volumes[i]
    return np.array([input_vec])


def calculate_output(data):
    # print(list(map(int,(data.time))))
    # input("")
    open_prices = data['open']
    if np.log(open_prices[1]/open_prices[0]) > 0.01:
        return 1
    if np.log(open_prices[1]/open_prices[0]) < -0.01:
        return 2
    else:
        return 0

model = train_model()
start_date = datetime(2018, 3, 1)
end_date = datetime(2018, 5, 1)
alg = TNG(start_date, end_date)
alg.addInstrument("ethbtc")
alg.addTimeframe("ethbtc", 60)

i = 0
def onBar(instrument):
    global model, i
    i += 1
    if i < 6:
        return
    pred = model.predict_classes(calculate_input(instrument.rates[1:7]))
    if pred == 1:
        alg.buy()
    elif pred == 2:
        alg.sell()
    
alg.run_backtest(onBar)
new_stat = bs.BacktestStatistics(alg.positions)
new_stat.backtest_results()