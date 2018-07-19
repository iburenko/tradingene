import tng.algorithm_backtest.tng as tng
from datetime import datetime
import tng.backtest_statistics.backtest_statistics as bs
import pandas as pd

name = "Cornucopia"
regime = "SP"
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 2, 1)

alg = tng.TNG(name, regime, start_date, end_date)

alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 30)

# df = pd.DataFrame(columns = ['time', 'open', 'high', 'low', 'close', 'vol'])


def onBar(instrument):
    # global df
    # to_append = pd.DataFrame([[int(instrument.rates['time'][1]*1000),
    #         instrument.rates['open'][1],
    #         instrument.rates['high'][1],
    #         instrument.rates['low'][1],
    #         instrument.rates['close'][1],
    #         instrument.rates['vol'][1]]], columns = ['time', 'open', 'high', 'low', 'close', 'vol'])
    #print(to_append)
    # df = df.append(to_append, ignore_index = True)
    print(instrument.time)
    print(instrument.adx().adx[1])
    print(instrument.aroon().up[1])
    print(instrument.atr()[1])
    print(instrument.bollinger().top[1])
    print(instrument.cci()[1])
    # print(instrument.chande()[1])
    print(instrument.keltner().basis[1])
    # print(instrument.macd().macd[1])
    print(instrument.momentum()[1])
    print(instrument.ppo()[1])
    # print(instrument.stochastic().k[1])
    print(instrument.williams()[1])
    print("======================================")
    # if instrument.open[1] > instrument.close[1]:
    #     # If price goes down during the day then sell;
    #     alg.sell()
    # elif instrument.open[1] < instrument.close[1]:
    #     # If price goes up during the day then buy;
    #     alg.buy()
    # else:
    #     # If price did not change then do nothing;
    #     pass


alg.run_backtest(onBar)
# df.to_csv("btcusd30.csv", index = False, header = False)
# new_stat = bs.BacktestStatistics(alg.positions)
# new_stat.backtest_results()
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
