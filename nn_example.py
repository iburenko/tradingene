from datetime import datetime
from time import time
from tng.data.load import import_data
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.initializers import he_normal, he_uniform
from keras.layers.normalization import BatchNormalization
import numpy as np
import cProfile
import pstats


def train_model():
    start_date = datetime(2018, 1, 1)
    end_date = datetime(2018, 4, 1)
    ticker = "ethbtc"
    timeframe = 10
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
    model.fit(data['train_input'], data['train_output'], epochs=100)
    loss, acc = model.evaluate(data['validation_input'], data['validation_output'])
    print(acc)

def create_model():
    model = Sequential()
    model.add(Dense(units=100, activation='tanh', input_dim=10, kernel_initializer=he_uniform(1)))
    model.add(Dense(100, activation='tanh'))
    model.add(Dense(50, activation='tanh'))
    model.add(Dense(1, activation='tanh'))
    model.compile(
        loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
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
    return input_vec


def calculate_output(data):
    # print(list(map(int,(data.time))))
    # input("")
    open_prices = data['open']
    if open_prices[0] > open_prices[1]:
        return 1
    else:
        return 0

train_model()

def onBar(instrument):
    pass
