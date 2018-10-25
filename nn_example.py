from datetime import datetime
from tradingene.data.load import import_data, import_candles
from tradingene.algorithm_backtest.tng import TNG
import tradingene.backtest_statistics.backtest_statistics as bs
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.initializers import he_uniform
from keras.layers.normalization import BatchNormalization
import keras
import numpy as np
import pandas as pd


def train_model():
    start_date = datetime(2018, 1, 1)
    end_date = datetime(2018, 3, 31)
    ticker = "btcusd"
    timeframe = 60
    lookback = 5
    lookforward = 2
    inds = {'sma':(10, 'open'), 'ema':(3), 'rsi':(), 'apo':(), \
            'atr':(), 'cci':(), 'chande':(), \
            'momentum': (), 'ppo':(), 'roc':(), \
            'trima':(), 'williams':(),\
            'bollinger':(), 'macd':(), 'keltner':(),
            'stochastic':()}
    #inds = {'sma':(11, 'open'), 'keltner':(8),'roc':(3)}
    data = import_data(
        ticker, timeframe, start_date, end_date, 
        calculate_input=calculate_input,
        lookback=lookback, 
        calculate_output=calculate_output, 
        lookforward=lookforward,
        split = (70, 30, 0), indicators = inds,
    )
    # data = import_candles(
    #     ticker,
    #     timeframe,
    #     start_date,
    #     end_date,
    #     indicators=inds
    # )

    model = create_model(data)
    outputs = keras.utils.to_categorical(data['train_output'], num_classes=3)
    model.fit(data['train_input'], outputs, epochs=10)
    val_outpus = keras.utils.to_categorical(data['validation_output'], num_classes = 3)
    loss, acc = model.evaluate(data['validation_input'], val_outpus)
    print(loss, acc)
    return model

def create_model(data):
    model = Sequential()
    model.add(Dense(units=100, activation='tanh', input_dim=10, kernel_initializer=he_uniform(1)))
    model.add(Dense(100, activation='tanh'))
    model.add(Dense(3, activation='softmax'))
    model.compile(
        loss='categorical_crossentropy', optimizer=keras.optimizers.Nadam(), metrics=['accuracy'])
    return model


def calculate_input(data):
    input_vec = np.zeros(10)
    open_prices = data['open']
    volumes = data['vol']
    print(data['ema'])
    input("")
    for i in range(5):
        input_vec[i] = open_prices[i]
        input_vec[i + 5] = volumes[i]
    return np.array([input_vec])

def calculate_output(data):
    open_prices = data['open']
    if np.log(open_prices[1]/open_prices[0]) > 0.007:
        return 2
    if np.log(open_prices[1]/open_prices[0]) < -0.007:
        return 0
    else:
        return 1
    

model = train_model()
start_date = datetime(2018, 4, 1)
end_date = datetime(2018, 5, 1)
alg = TNG(start_date, end_date)
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 60)

def onBar(instrument):
    pred = model.predict_classes(calculate_input(instrument.rates[1:7]))
    if pred == 0:
        alg.buy()
    elif pred == 2:
        alg.sell()
    
alg.run_backtest(onBar)
new_stat = bs.BacktestStatistics(alg)
new_stat.backtest_results()