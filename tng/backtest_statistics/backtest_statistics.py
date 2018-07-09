import time
import datetime
import numpy as np


class BacktestStatistics:
    def __init__(self, positions):
        if positions[-1].close_time == 0:
            self.all_positions_ = positions[:-1]
        else:
            self.all_positions_ = positions
        self.winning_trades_ = [
            pos for pos in self.all_positions_ if pos.profit >= 0
        ]
        self.losing_trades_ = [
            pos for pos in self.all_positions_ if pos.profit < 0
        ]
        self.number_of_positions = len(self.all_positions_)
        self.PnL = 0
        self.max_drawdown = 0
        self.reliability = 0
        self.risk_reward_ratio = 0
        self.average_trade = 0
        self.average_time_in_trade = 0
        self.average_deals_per_day = 0
        self.profit = 0
        self.loss = 0
        self.average_winning_trade = 0
        self.average_losing_trade = 0
        self.winning_trades = len(self.winning_trades_)
        self.losing_trades = len(self.losing_trades_)
        self.largest_winning_trade = 0
        self.largest_losing_trade = 0
        self.average_time_in_winning_trade = 0
        self.average_time_in_losing_trade = 0
        self.max_consecutive_winners = 0
        self.max_consecutive_losers = 0

    def calculate_PnL(self):
        pnl = 0
        for pos in self.all_positions_:
            pnl += pos.profit
        return float(pnl)

    def calculate_reliability(self):
        return len(self.winning_trades_) / len(self.all_positions_)

    def calculate_RRR(self):
        average_win = self.calculate_AWT()
        average_loss = self.calculate_ALT()
        return average_loss / average_win

    def calculate_drawdown(self):
        cumulative_profit = np.zeros((len(self.all_positions_) + 1))
        profit = 0
        i = 1
        for pos in self.all_positions_:
            profit += pos.profit
            cumulative_profit[i] = profit
            i += 1
        drawdown_values = np.array([])
        drawdown_lens = np.array([])
        drawdown_price_array = np.array([])
        drawdown_flag = 0
        for i in range(1, len(cumulative_profit)):
            diff = cumulative_profit[i] - cumulative_profit[i - 1]
            if drawdown_flag:
                if cumulative_profit[i] > drawdown_price_array[0]:
                    drawdown_flag = 0
                    drawdown_len = i - 1 - drawdown_start_pos
                    drawdown = \
                            drawdown_price_array[0] - np.min(drawdown_price_array)
                    drawdown_price_array = np.array([])
                    drawdown_values = np.append(drawdown_values, drawdown)
                    drawdown_lens = np.append(drawdown_lens, drawdown_len)
                else:
                    drawdown_price_array = np.append(drawdown_price_array, \
                                                     cumulative_profit[i])
            else:
                if diff < 0:
                    drawdown_flag = 1
                    drawdown_start_pos = i - 1
                    drawdown_price_array = np.append(
                        drawdown_price_array,
                        [cumulative_profit[i - 1], cumulative_profit[i]])
                else:
                    pass
        drawdown_len = i - 1 - drawdown_start_pos
        drawdown = \
                drawdown_price_array[0] - np.min(drawdown_price_array)
        drawdown_price_array = np.array([])
        drawdown_values = np.append(drawdown_values, drawdown)
        drawdown_lens = np.append(drawdown_lens, drawdown_len)
        drawdown = np.max(drawdown_values)
        drawdown_len = drawdown_lens[np.argmax(drawdown_values)]
        return (drawdown, int(drawdown_len))

    def calculate_AT(self):
        pnl = self.calculate_PnL()
        return pnl / self.number_of_positions

    def calculate_ATT(self):
        overall_time = 0
        for pos in self.all_positions_:
            open_time = datetime.datetime(*(time.strptime(str(pos.open_time), \
                                           "%Y%m%d%H%M%S")[0:6]))
            close_time = datetime.datetime(*(time.strptime(str(pos.close_time), \
                                           "%Y%m%d%H%M%S")[0:6]))
            diff = close_time - open_time
            trade_time = 1440 * diff.days + diff.seconds / 60
            overall_time += trade_time
        return overall_time / self.number_of_positions

    def calculate_ADPD(self):
        first_pos = self.all_positions_[0]
        last_pos = self.all_positions_[-1]
        open_time = datetime.datetime(*(time.strptime(str(first_pos.open_time), \
                                           "%Y%m%d%H%M%S")[0:6]))
        close_time = datetime.datetime(*(time.strptime(str(last_pos.close_time), \
                                        "%Y%m%d%H%M%S")[0:6]))
        diff = close_time - open_time
        overall_days = diff.days
        return self.number_of_positions / (overall_days + 1)

    def calculate_profit(self):
        profit = 0
        for pos in self.winning_trades_:
            profit += pos.profit
        return float(profit)

    def calculate_loss(self):
        loss = 0
        for pos in self.losing_trades_:
            loss += pos.profit
        return float(loss)

    def calculate_AWT(self):
        profit = self.calculate_profit()
        return profit / self.winning_trades

    def calculate_ALT(self):
        loss = self.calculate_loss()
        return loss / self.losing_trades

    def calculate_WT(self):
        return self.winning_trades

    def calculate_LT(self):
        return self.losing_trades

    def calculate_LWT(self):
        profits = [pos.profit for pos in self.winning_trades_]
        return float(max(profits))

    def calculate_LLT(self):
        losses = [pos.profit for pos in self.losing_trades_]
        return float(min(losses))

    def calculate_ATWT(self):
        overall_time = 0
        for pos in self.winning_trades_:
            open_time = datetime.datetime(*(time.strptime(str(pos.open_time), \
                                           "%Y%m%d%H%M%S")[0:6]))
            close_time = datetime.datetime(*(time.strptime(str(pos.close_time), \
                                           "%Y%m%d%H%M%S")[0:6]))
            diff = close_time - open_time
            trade_time = 1440 * diff.days + diff.seconds / 60
            overall_time += trade_time
        return overall_time / self.winning_trades

    def calculate_ATLT(self):
        overall_time = 0
        for pos in self.losing_trades_:
            open_time = datetime.datetime(*(time.strptime(str(pos.open_time), \
                                           "%Y%m%d%H%M%S")[0:6]))
            close_time = datetime.datetime(*(time.strptime(str(pos.close_time), \
                                           "%Y%m%d%H%M%S")[0:6]))
            diff = close_time - open_time
            trade_time = 1440 * diff.days + diff.seconds / 60
            overall_time += trade_time
        return overall_time / self.losing_trades

    def calculate_MCW(self):
        cons_winners = list()
        current_cons_winners = 0
        flag = 0
        for pos in self.all_positions_:
            if pos.profit >= 0:
                current_cons_winners += 1
                flag = 1
            else:
                if flag:
                    cons_winners.append(current_cons_winners)
                    current_cons_winners = 0
                flag = 0
        return max(cons_winners)

    def calculate_MCL(self):
        cons_losses = list()
        current_cons_losses = 0
        flag = 0
        for pos in self.all_positions_:
            if pos.profit < 0:
                current_cons_losses += 1
                flag = 1
            else:
                if flag:
                    cons_losses.append(current_cons_losses)
                    current_cons_losses = 0
                flag = 0
        return max(cons_losses)

    def _calculate_correlation(self):
        price_array = np.zeros((len(self.all_positions_)))
        profit_array = np.zeros((len(self.all_positions_)))
        i = 0
        for pos in self.all_positions_:
            price_array[i] = pos.trades[0].open_price
            profit_array[i] = pos.profit
            i += 1
        corr = np.corrcoef(price_array, profit_array)[0][1]
        return corr

    def backtest_results(self):
        all_stats = [method for method in dir(BacktestStatistics) \
                            if callable(getattr(BacktestStatistics, method)) \
                            if method.startswith('calculate_')]
        for method in all_stats:
            explanatory_str = method.replace("calculate_", "") + " = \t"
            print(explanatory_str, eval("self." + method)())
