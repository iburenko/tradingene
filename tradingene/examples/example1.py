from datetime import datetime
from tng.algorithm_backtest.tng import TNG
from tng.backtest_statistics import backtest_statistics as bs

name = "example1"
regime = "SP"
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 5, 1)
timeframe = 1440

alg = TNG(name, regime, start_date, end_date)
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", timeframe)
positionId = None


def onBar(instrument):
    global positionId
    if positionId is None:
        if instrument.macd().histogram[2] > instrument.macd().histogram[1]:
            positionId = alg.openLong(1)
        if instrument.macd().histogram[2] < instrument.macd().histogram[1]:
            positionId = alg.openShort(1)
    else:
        if instrument.macd().histogram[2] > instrument.macd().histogram[1] and\
           alg.getPositionSide(positionId) <=0:
            alg.closePosition(positionId)
            positionId = alg.openLong(1)
        if instrument.macd().histogram[2] < instrument.macd().histogram[1] and \
           alg.getPositionSide(positionId) >= 0:
            alg.closePosition(positionId)
            positionId = alg.openShort(1)

alg.run_backtest(onBar)
stat = bs.BacktestStatistics(alg)
stat.backtest_results()
