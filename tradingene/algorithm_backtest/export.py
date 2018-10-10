from tng.data.load import import_candles
import tng.ind.ind as tngind
import pandas as pd
import numpy as np

class Export:

    def __init__(self, alg_):
        self.alg = alg_

    def export_results(self, indicators, lookback, filename=None):
        dict_values = dict()
        for ind_name, ind_params in indicators.items():
            for class_name in dir(tngind):
                if ind_name == class_name[3:].lower():
                    break
            if not isinstance(ind_params, tuple):
                ind_params = (ind_params, )
            new_ind = eval("tngind." + class_name + str(ind_params))
            explanatory_str = ""
            rates = list(self.alg.instruments)[0].candles
            ind_values = new_ind.calculateRates(rates)
            for key in ind_values.keys():
                dict_values[key + explanatory_str] = ind_values[key]

        size = lookback*(len(dict_values)+5)+4
        positions = len(self.alg.positions)
        ans = np.zeros((positions,size))
        data = np.full((size), np.nan)
        ind = 0
        current_index = -1
        candles = list(self.alg.instruments)[0].candles
        df_columns = ['time', 'price', 'side', 'profit']
        for i in range(lookback):
            df_columns += [
                        'open'+str(i), 
                        'high'+str(i), 
                        'low'+str(i), 
                        'close'+str(i), 
                        'volume'+str(i)
                    ]
        for key in dict_values.keys():
            for i in range(lookback):
                df_columns += [key+str(i)]
        for pos in self.alg.positions:
            trade = pos.trades[0]
            while candles[current_index]['time'] < trade.open_time:
                current_index -= 1
            top_index = current_index+lookback+1
            if top_index >= 1:
                continue
            data[0:4] = np.array([int(trade.open_time), trade.open_price, int(trade.side), pos.profit])
            if trade.open_time != candles[current_index]['time']:
                for i, candle in enumerate(candles[current_index+2:top_index+1]):
                        data[4+i*5:4+(i+1)*5] = list(candle)[1:]
                i = 0
                for key, value in dict_values.items():
                    length = -current_index - 1 + top_index
                    start_ind = 4+lookback*5 + i*length
                    end_ind = 4+lookback*5+ (i+1)*length
                    data[start_ind:end_ind] = value[current_index+2:top_index+1]
                    i += 1
            else:
                if top_index == 0:
                    for i, candle in enumerate(candles[current_index+1:]):
                        data[4+i*5:4+(i+1)*5] = list(candle)[1:]
                    i = 0
                    for key, value in dict_values.items():
                        length = -current_index - 1
                        start_ind = 4+lookback*5 + i*length
                        end_ind = 4+lookback*5+(i+1)*length
                        data[start_ind:end_ind] = value[current_index+1:]
                        i += 1
                else:
                    for i, candle in enumerate(candles[current_index+1:top_index]):
                        data[4+i*5:4+(i+1)*5] = list(candle)[1:]
                    i = 0
                    for key, value in dict_values.items():
                        length = -current_index - 1 + top_index
                        start_ind = 4+lookback*5 + i*length
                        end_ind = 4+lookback*5+(i+1)*length
                        data[start_ind:end_ind] = value[current_index+1:top_index]
                        i += 1
            ans[ind] = data
            ind += 1
        ans = pd.DataFrame(ans[:ind], columns=df_columns)
        if filename is None:
            ans.to_csv("results.csv", index=False)
        else:
            assert isinstance(filename, str)
            ans.to_csv(filename+".csv", index=False)