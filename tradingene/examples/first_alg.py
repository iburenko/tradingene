from datetime import datetime
from tradingene.data.load import import_data
from tradingene.algorithm_backtest.tng import TNG
import tradingene.backtest_statistics.backtest_statistics as bs

start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 2, 1)
ticker = "btcusd"
timeframe = 60


def onBar(instrument):
    bollinger10 = instrument.bollinger(10)  # Retrieving the value of the Bollinger indicator of period 10.
    if instrument.close[1] > bollinger10.top[1]:  # If the price soars above the Bollinger top line...
        alg.buy() 
    elif instrument.close[1] < bollinger10.bottom[1]:  # If the price falls below the Bollinger bottom line...
        alg.sell()


alg = TNG(start_date, end_date)  # Creating an instance of the class (TNG) to run the algorithm within.
alg.addInstrument(ticker)  # Adding an instrument.
alg.addTimeframe(ticker, timeframe)  # Adding a time frame.
alg.run_backtest(onBar)  # Backtesting...

stat = bs.BacktestStatistics(alg)  # Retrieving statistics of the backtest

pnl = stat.calculate_PnL()
num_positions = stat.calculate_number_of_trades()
print("pnl=%f, num_positions=%d" % (pnl, num_positions))

stat.backtest_results()  # Displaying the backtest statistics
