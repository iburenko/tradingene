import tng.algorithm_backtest.tng as tng
from datetime import datetime
import tng.backtest_statistics.backtest_statistics as bs

name = "Cornucopia"
regime = "SP"
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 2, 1)

alg = tng.TNG(name, regime, start_date, end_date)

alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 1440)


def onBar(instrument):
    print(instrument.time, "ema(10)[1] = ",instrument.ema(10)[1], \
                           "rsi(10)[1] = ",instrument.rsi(10)[1])
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
new_stat = bs.BacktestStatistics(alg.positions)
new_stat.backtest_results()
#new_stat.calculate_ATT()
# new_stat.print_statistics()
# print(new_stat.calculate_drawdown())
# print(new_stat.calculate_PnL())
# print(new_stat.calculate_AT())
# print(new_stat.calculate_profit())
# print(new_stat.calculate_loss())
# print(new_stat.calculate_AWT())
# print(new_stat.calculate_ALT())
# print(new_stat.calculate_LWT())
# print(new_stat.calculate_LLT())
# print(new_stat.calculate_MCW())
# print(new_stat.calculate_MCL())