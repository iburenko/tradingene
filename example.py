import tng.algorithm_backtest.tng as tng
from datetime import datetime

name = "Cornucopia"
regime = "SP"
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 2, 1)

alg = tng.TNG(name, regime, start_date, end_date)

alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 1440)


def onBar(instrument):
    if instrument.open[1] > instrument.close[1]:
        # If price goes down during the day then sell;
        alg.sell()
    elif instrument.open[1] < instrument.close[1]:
        # If price goes up during the day then buy;
        alg.buy()
    else:
        # If price did not change then do nothing;
        pass


alg.run_backtest(onBar)
