from datetime import datetime
from tradingene.data.load import import_data
from tradingene.algorithm_backtest.tng import TNG
import tradingene.backtest_statistics.backtest_statistics as bs
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.initializers import he_normal, he_uniform
from keras.layers.normalization import BatchNormalization
import keras
import numpy as np

_lookback = 9  # How many prior candle bars each train sample embraces.
_num_features = _lookback  # The number of features. This depends on how you implement the "calculate_input()" function.
# This time the number of features equals the "lookback" period.
_lookforward = 3  # How far in the future the algorithm "looks" and foresees.
_num_classes = 3  # The number of classes depends of what the "calculate_output()" fuction returns (see below)
_num_epochs = 100  # The number of epochs to train your model through.
_timeframe = 60  # The time frame.
_ticker = "btcusd"  # The ticker.
_start_train_date = datetime(2017, 5, 1)  # When a train period starts...
_end_train_date = datetime(
    2017, 6, 1)  # When the train period ends and the test starts...
_end_test_date = datetime(2017, 6, 6)  # When the test ends...

_threshold = 0.001  # A threshold to devide outputs into classes (please refer to the "calculate_output()" function below)

_alg = None  # An instance of the "TNG" class used for simulated trading

#_scaler = None


def prepare_model():
    global _lookback, _lookforward, _num_features, _timeframe, _ticker, _scaler

    data = import_data(
        _ticker,
        _timeframe,
        _start_train_date,
        _end_train_date,
        calculate_input,
        _lookback,
        calculate_output,
        _lookforward,
        split=(
            100, 0, 0
        )  # This time we need only a train set (100% for train set, 0% for test and validation ones)
    )

    #scaler = StandardScaler()
    #scaler.fit( data['train_input'] )
    #train_input_scaled = scaler.transform( data['train_input'] )

    # Creating a model...
    model = Sequential()  # Creating a model class instance
    # The number of nodes in the first hidden layer equals the number of features multiplied by 2
    model.add(
        Dense(
            units=_num_features * 2,
            activation='tanh',
            input_dim=_num_features,
            kernel_initializer=he_uniform(1)))
    # Adding another hidden layer
    model.add(Dense(_num_features * 2, activation='tanh'))
    # Adding an output layer
    model.add(Dense(_num_classes, activation='softmax'))
    # Compiling the model
    model.compile(
        loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

    one_hot_train_outputs = keras.utils.to_categorical(
        data['train_output'],
        num_classes=_num_classes)  # Performing one-hot encoding
    model.fit(
        data['train_input'], one_hot_train_outputs,
        epochs=_num_epochs)  # Training the model
    return model


# end of load_data


def calculate_input(data):
    global _lookback  # How deep in the past the network "looks"

    input_vec = np.zeros(_num_features)  # A vector to store inputs
    for i in range(_lookback):
        input_vec[i] = (data['open'][i] - data['close'][0]) / data['close'][0]
    return np.array([input_vec])


def calculate_output(data):
    global _lookforward

    for i in range(_lookforward):
        if (
                data['high'][i] - data['open'][0]
        ) / data['open'][0] > _threshold:  # If price breaks the threshold up...
            return [2]  # ... it makes class "2"
        elif (
                data['low'][i] - data['open'][0]
        ) / data['open'][0] < -_threshold:  # If price breaks the threshold down...
            return [0]  # ... it make class "0"
    return [
        1
    ]  # If the threshold hasn/t been broken neither up nor down - it's class "1"


def onBar(instrument):
    global _alg, _model, _lookback, _scaler

    inp = calculate_input(instrument.rates[1:_lookback + 1])
    #inp = _scaler.transform( inp )

    prediction = _model.predict_classes([inp])[0]
    if prediction == 2:  # Class "2" predicts price to surge up
        _alg.buy()
        tp = instrument.rates[0]['open'] * _threshold  # Setting the take profit as big as the price threshold
        sl = tp  # Setting the stop loss equal to the take profit.
        _alg.setTP(profit=tp)
        _alg.setSL(loss=sl)
    elif prediction == 0:  # Class "0" predicts price to fall down
        _alg.sell()
        tp = instrument.rates[0]['open'] * _threshold  # Setting the take profit as big as the price threshold
        sl = tp  # Setting the stop loss equal to the take profit.
        _alg.setTP(profit=tp)
        _alg.setSL(loss=sl)


# end of onBar()

_model = prepare_model()  # Creating an ML-model.
_alg = TNG(
    _end_train_date,
    _end_test_date)  # Creating an instance of environment to run algorithm in.
_alg.addInstrument(_ticker)  # Adding an instrument.
_alg.addTimeframe(_ticker, _timeframe)  # Adding a time frame.
_alg.run_backtest(onBar)  # Backtesting...

stat = bs.BacktestStatistics(_alg)  # Retrieving statistics of the backtest

pnl = stat.calculate_PnL()
num_positions = stat.calculate_number_of_trades()
print("pnl=%f, num_positions=%d" % (pnl, num_positions))

stat.backtest_results()  # Displaying the backtest statistics
