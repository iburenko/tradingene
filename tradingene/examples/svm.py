from datetime import datetime
from tradingene.data.load import import_data
from tradingene.algorithm_backtest.tng import TNG
import tradingene.backtest_statistics.backtest_statistics as bs
from sklearn.svm import SVC
import numpy as np

num_features = lookback = 3
lookforward = 1  # How far in the future the algorithm "looks" and foresees.
timeframe = 60 
ticker = "btcusd"
start_train_date = datetime(2018, 2, 25)
end_train_date = datetime(2018, 3, 5)
end_test_date = datetime(2018, 3, 15)

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

    # Creating an SVC model
    model = SVC(tol=1e-4, degree=4)
    # Reshaping the inputs to be passed into the "fit" function
    train_output = np.reshape(data['train_output'], (np.shape(data['train_output'])[0], ))
    model.fit(data['train_input'], train_output)
    return model
# end of load_data


def calculate_input(data):
    input_vec = np.zeros(num_features)  # A vector to store inputs
    for i in range(lookback):
        input_vec[i] = 100.0 * (
            data['open'][i] - data['close'][0]) / data['close'][0]
    return input_vec


def calculate_output(data):
    if data['close'][lookforward - 1] > data['open'][0] * 1.01:
        return 1
    elif data['close'][lookforward - 1] * 1.01 < data['open'][0]:
        return -1
    else:
        return 0


def onBar(instrument):
    inp = calculate_input(
        instrument.rates[1:lookback + 1])  # Calculating inputs
    prediction = model.predict([inp])[0]  # Making prediction
    if prediction > 0:
        alg.buy()
    elif prediction < 0:
        alg.sell()
# end of onBar()

model = prepare_model()  # Creating an ML-model.
alg = TNG(end_train_date, end_test_date)  # Creating an instance of environment to run algorithm in.
alg.addInstrument(ticker)  # Adding an instrument.
alg.addTimeframe(ticker, timeframe)  # Adding a time frame.
alg.run_backtest(onBar)  # Backtesting...

stat = bs.BacktestStatistics(alg)  # Retrieving statistics of the backtest

pnl = stat.calculate_PnL()
num_positions = stat.calculate_number_of_trades()
print("pnl=%f, num_positions=%d" % (pnl, num_positions))

stat.backtest_results()  # Displaying the backtest statistics
