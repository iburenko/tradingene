from datetime import datetime
from time import time
from tng.algorithm_backtest.instrument import Instrument
from tng.ml.load import import_data
from keras.models import Sequential
from keras.layers import Dense
import numpy as np

def main():
    train_start_date = datetime(2018, 1, 1)
    train_end_date = datetime(2018, 4, 1)
    test_start_date = datetime(2018, 4, 1)
    test_end_date = datetime(2018, 5, 1)
    ticker = "ethbtc"
    timeframe = 60
    train_data = import_data(
        ticker, timeframe, train_start_date, train_end_date
    )
    test_data = import_data(
        ticker, timeframe, test_start_date, test_end_date
    )
    train_dataset_len = len(train_data['time'])
    test_dataset_len = len(test_data['time'])
    lookback = 5
    X_train = np.zeros((train_dataset_len - 1, 10))
    Y_train = np.zeros((train_dataset_len - 1, 1))
    for i in range(train_dataset_len - lookback - 1):
        X_train[i] = calculate_input(train_data[i+1:])
        Y_train[i] = calculate_output(train_data[i:])
    nn_model = create_model()
    nn_model.fit(X_train, Y_train, epochs = 20, batch_size = 128)
    X_test = np.zeros((test_dataset_len, 10))
    Y_test = np.zeros((test_dataset_len, 1))
    for i in range(test_dataset_len - lookback - 1):
        X_test[i] = calculate_input(train_data[i+1:])
        Y_test[i] = calculate_output(train_data[i:])
    score = nn_model.evaluate(X_test, Y_test, batch_size = 128)
    print(score)
    
def create_model():
    model = Sequential()
    model.add(Dense(units = 100, activation = 'relu', input_dim = 10))
    model.add(Dense(100, activation = 'relu'))
    model.add(Dense(1, activation = 'sigmoid'))
    model.compile(
        loss = 'binary_crossentropy',
        optimizer = 'sgd',
        metrics = ['accuracy']
    )
    return model

def calculate_input(data):
    input_vec = np.zeros(10)
    open_prices = data['open']
    volumes = data['vol']
    for i in range(5):
        input_vec[i] = open_prices[i]
        input_vec[i+5] = volumes[i]
    return input_vec

def calculate_output(data):
    open_prices = data['open']
    if open_prices[0] > open_prices[1]:
        return 1
    else:
        return -1

main()