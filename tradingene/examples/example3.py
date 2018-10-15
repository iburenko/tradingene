from datetime import datetime
from tradingene.algorithm_backtest.tng import TNG
import tradingene.backtest_statistics.backtest_statistics as bs

name = "example1"
regime = "SP"
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 2, 1)
timeframe = 30

alg = TNG(name, regime, start_date, end_date)
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", timeframe)
positionId = None


def onBar(instrument):
    global positionId
    if positionId == None:
        if instrument.close[1] > instrument.bollinger().top[1] and \
           instrument.close[2] < instrument.bollinger().top[2]:
            positionId = alg.openLong(1)
        if instrument.close[1] < instrument.bollinger().bottom[1] and \
           instrument.close[2] > instrument.bollinger().bottom[2]:
            positionId = alg.openShort(1)
    else:
        if instrument.close[1] > instrument.bollinger().ma[1] and \
           instrument.close[2] < instrument.bollinger().ma[2] and \
           alg.getPositionSide(positionId) <=0:
            alg.closePosition(positionId)
            positionId = None
        if instrument.close[1] < instrument.bollinger().ma[1] and \
           instrument.close[2] > instrument.bollinger().ma[2] and \
           alg.getPositionSide(positionId) >= 0:
            alg.closePosition(positionId)
            positionId = None


alg.run_backtest(onBar)
new_stat = bs.BacktestStatistics(alg)
new_stat.backtest_results()
