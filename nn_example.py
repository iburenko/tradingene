from datetime import datetime
from time import time
from tng.algorithm_backtest.instrument import Instrument
from tng.ml.load import import_data
from keras.models import Sequential
from keras.layers import Dense
import numpy as np


def main():
    train_start_date = datetime(2018, 1, 1)
    train_end_date = datetime(2018, 2, 1)
    ticker = "ethbtc"
    timeframes = [1,2,3,5,10,15,30,60,120,240,720,1440]
    for timeframe in timeframes:
        inds = {'sma':(10, 'open'), 'ema':(3), 'rsi':(), 'apo':(), \
                'atr':(), 'cci':(), 'chande':(), \
                'momentum': (), 'ppo':(), 'roc':(), \
                'trima':(), 'williams':()}
        #inds = {'sma': 10}
        t = time()
        data = import_data(
            ticker, timeframe, train_start_date, train_end_date, split = (50, 25, 25), indicators = inds
        )
        print(timeframe, time() - t)
        # print(len(data['train']))
        # if 'validation' in data.keys():
        #     print(len(data['validation']))
        # print(len(data['test']))


def create_model():
    model = Sequential()
    model.add(Dense(units=100, activation='relu', input_dim=10))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(
        loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
    return model


def calculate_input(data):
    input_vec = np.zeros(10)
    open_prices = data['open']
    volumes = data['vol']
    for i in range(5):
        input_vec[i] = open_prices[i]
        input_vec[i + 5] = volumes[i]
    return input_vec


def calculate_output(data):
    open_prices = data['open']
    if open_prices[0] > open_prices[1]:
        return 1
    else:
        return -1


main()
