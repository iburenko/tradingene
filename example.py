import tng.algorithm_backtest.tng as tng
from datetime import datetime
import tng.backtest_statistics.backtest_statistics as bs
import pandas as pd

name = "Cornucopia"
regime = "SP"
start_date = datetime(2018, 4, 1)
end_date = datetime(2018, 5, 1)

alg = tng.TNG(name, regime, start_date, end_date)
alg.addInstrument("btcusd")
alg.addTimeframe("btcusd", 1440)

# df = pd.DataFrame(columns = ['time', 'open', 'high', 'low', 'close', 'vol'])


def onBar(instrument):
    print(instrument.time)
    print(instrument.close[1:50])
    input("")
    # print("ad = ", instrument.ad()[1])
    # print("adx = ", instrument.adx().adx[1])
    # print("apo = ", instrument.apo()[1])
    # print("aroon = ", instrument.aroon().up[1])
    # print("atr = ", instrument.atr()[1])
    # print("bollinger = ", instrument.bollinger().top[1])
    # print("cci = ", instrument.cci()[1])
    # print("chande = ", instrument.chande()[1])
    # print("ema = ", instrument.ema(9)[1], instrument.close[1])
    # print("keltner = ", instrument.keltner().basis[1])
    # print("macd = ", instrument.macd().macd[1])
    # print("momentum = ", instrument.momentum()[1])
    # print("ppo = ", instrument.ppo()[1])
    # print("roc = ", instrument.roc()[1])
    # print("sma = ", instrument.sma()[1])
    # print("rsi = ", instrument.rsi()[1])
    # print("stochastic = ", instrument.stochastic().k[1])
    # print("trima = ", instrument.trima()[1])
    # print("williams = ",instrument.williams()[1])
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
