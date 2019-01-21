from datetime import datetime
from tradingene.data.load import import_data
from tradingene.algorithm_backtest.tng import TNG
import tradingene.backtest_statistics.backtest_statistics as bs
from keras.models import Sequential
from keras.layers import Dense
from keras.initializers import he_uniform
import numpy as np

num_features = lookback = 7
lookforward = 1 
num_epochs = 50 
timeframe = 60 
ticker = "btcusd"
start_train_date = datetime(2017, 6, 1)
end_train_date = datetime(2017, 7, 1)
end_test_date = datetime(2017, 7, 6)

alg = None 

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
    model1 = create_and_train_model(data)
    model2 = create_and_train_model(data)
    model3 = create_and_train_model(data)
    return (model1, model2, model3)
# end of load_data


def create_and_train_model(data):
    model = Sequential()
    model.add(
        Dense(
            units=num_features,
            activation='tanh',
            input_dim=num_features,
            kernel_initializer=he_uniform(1)))
    model.add(Dense(num_features, activation='tanh'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mean_squared_error', optimizer='sgd')
    model.fit(data['train_input'], data['train_output'], epochs=num_epochs)
    return model
# end of create_and_train_model


def calculate_input(data):
    input_vec = np.zeros(num_features)  # A vector to store inputs
    for i in range(lookback):
        input_vec[i] = np.log(data['open'][i] / data['close'][0])
    return np.array([input_vec])


def calculate_output(data):
    return (data['close'][lookforward - 1] - data['open'][0]) / data['open'][0]


def onBar(instrument):
    inp = calculate_input(instrument.rates[1:lookback + 1])
    prediction1 = model1.predict([inp])
    prediction2 = model2.predict([inp])
    prediction3 = model3.predict([inp])
    if prediction1 > 0 and prediction2 > 0 and prediction3 > 0:  # If market rising is predicted...
        alg.buy()
    elif prediction1 < 0 and prediction2 < 0 and prediction3 < 0:  # If market falling is predicted...
        alg.sell()


model1, model2, model3 = prepare_model()
alg = TNG(end_train_date, end_test_date)
alg.addInstrument(ticker)
alg.addTimeframe(ticker, timeframe)
alg.run_backtest(onBar)

stat = bs.BacktestStatistics(alg)  # Retrieving statistics of the backtest

pnl = stat.calculate_PnL()  # Retrieving the PnL.
num_positions = stat.calculate_number_of_trades()  # Retrieving the number of trades done.
print("pnl=%f, num_positions=%d" % (pnl, num_positions))

stat.backtest_results()  # Displaying the backtest statistics
