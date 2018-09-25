import os, sys, subprocess
import time
import datetime
import numpy as np
from tng.plot.plot import plot_cs_prof


class BacktestStatistics:
    def __init__(self, alg):
        positions = alg.positions
        self.alg = alg
        self.all_positions_ = list()
        self.winning_trades_ = list()
        self.losing_trades_ = list()
        try:
            assert len(positions) > 0
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
            self.winning_trades = len(self.winning_trades_)
            self.losing_trades = len(self.losing_trades_)
        except AssertionError:
            print("No positions was open while backtest!")
        self.PnL = None
        self.max_drawdown = 0
        self.reliability = 0
        self.risk_reward_ratio = 0
        self.average_trade = 0
        self.average_time_in_trade = 0
        self.average_deals_per_day = 0
        self.profit = None
        self.loss = None
        self.average_winning_trade = None
        self.average_losing_trade = None
        self.largest_winning_trade = 0
        self.largest_losing_trade = 0
        self.average_time_in_winning_trade = 0
        self.average_time_in_losing_trade = 0
        self.max_consecutive_winners = 0
        self.max_consecutive_losers = 0
        self._calculated = 0

    def calculate_PnL(self):
        pnl = 0
        for pos in self.all_positions_:
            pnl += pos.profit
        if self.alg.positions and self.alg.positions[-1].close_time != 0:
            pnl += self.alg.positions[-1].profit
        self.PnL = pnl
        return pnl

    def calculate_number_of_trades(self):
        return self.number_of_positions

    def calculate_reliability(self):
        if self.number_of_positions == 0:
            return 0
        else:
            self.reliability = len(self.winning_trades_) / len(
                self.all_positions_)
            return self.reliability

    def calculate_RRR(self):
        if self.average_winning_trade is None:
            average_win = self.calculate_AWT()
        else:
            average_win = self.average_winning_trade
        if self.average_losing_trade is None:
            average_loss = self.calculate_ALT()
        else:
            average_loss = self.average_losing_trade
        if average_win == 0:
            return 0
        else:
            self.risk_reward_ratio = average_loss / average_win
            return self.risk_reward_ratio

    def calculate_drawdown(self):
        cumulative_profit = np.zeros((len(self.all_positions_) + 1))
        profit = 0
        drawdown = -1
        drawdown_len = -1
        drawdown_start_pos = 0
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
                diff = cumulative_profit[i] - cumulative_profit[i - 1]
                if diff < 0:
                    drawdown_flag = 1
                    drawdown_start_pos = i - 1
                    drawdown_price_array = np.append(
                        drawdown_price_array,
                        [cumulative_profit[i - 1], cumulative_profit[i]])
                else:
                    pass
        if drawdown_flag:
            drawdown_len = i - 1 - drawdown_start_pos
            drawdown = \
                    drawdown_price_array[0] - np.min(drawdown_price_array)
            drawdown_price_array = np.array([])
            drawdown_values = np.append(drawdown_values, drawdown)
            drawdown_lens = np.append(drawdown_lens, drawdown_len)
            drawdown = np.max(drawdown_values)
            drawdown_len = drawdown_lens[np.argmax(drawdown_values)]
        if drawdown == -1 and drawdown_len == -1:
            return (0, 0)
        else:
            self.max_drawdown = drawdown
            return (self.max_drawdown, int(drawdown_len))

    def calculate_AT(self):
        if self.PnL is None:
            pnl = self.calculate_PnL()
        else:
            pnl = self.PnL
        if self.number_of_positions == 0:
            return 0
        else:
            self.average_trade = pnl / self.number_of_positions
            return self.average_trade

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
        if self.number_of_positions == 0:
            return 0
        else:
            self.average_time_in_trade = overall_time / self.number_of_positions
            return self.average_time_in_trade

    def calculate_ADPD(self):
        if len(self.all_positions_) > 0:
            first_pos = self.all_positions_[0]
            last_pos = self.all_positions_[-1]
            open_time = datetime.datetime(*(time.strptime(str(first_pos.open_time), \
                                            "%Y%m%d%H%M%S")[0:6]))
            close_time = datetime.datetime(*(time.strptime(str(last_pos.close_time), \
                                            "%Y%m%d%H%M%S")[0:6]))
            diff = close_time - open_time
            overall_days = diff.days
            self.average_deals_per_day = self.number_of_positions / (
                overall_days + 1)
            return self.average_deals_per_day
        else:
            return 0

    def calculate_profit(self):
        profit = 0
        for pos in self.winning_trades_:
            profit += pos.profit
        if self.alg.positions:
            last_pos = self.alg.positions[-1]
            if last_pos.close_time != 0 and last_pos.profit > 0:
                profit += last_pos.profit
        self.profit = profit
        return profit

    def calculate_loss(self):
        loss = 0
        for pos in self.losing_trades_:
            loss += pos.profit
        if self.alg.positions:
            last_pos = self.alg.positions[-1]
            if last_pos.close_time != 0 and last_pos.profit < 0:
                loss += last_pos.profit
        self.loss = loss
        return loss

    def calculate_AWT(self):
        if self.profit is None:
            profit = self.calculate_profit()
        else:
            profit = self.profit
        if self.winning_trades == 0:
            return 0
        else:
            self.average_winning_trade = profit / self.winning_trades
            return self.average_winning_trade

    def calculate_ALT(self):
        if self.loss is None:
            loss = self.calculate_loss()
        else:
            loss = self.loss
        if self.losing_trades == 0:
            return 0
        else:
            self.average_losing_trade = loss / self.losing_trades
            return self.average_losing_trade

    def calculate_WT(self):
        return self.winning_trades

    def calculate_LT(self):
        return self.losing_trades

    def calculate_LWT(self):
        profits = [pos.profit for pos in self.winning_trades_]
        if profits:
            self.largest_winning_trade = max(profits)
            return self.largest_winning_trade
        else:
            return 0

    def calculate_LLT(self):
        losses = [pos.profit for pos in self.losing_trades_]
        if losses:
            self.largest_losing_trade = min(losses)
            return self.largest_losing_trade
        else:
            return 0

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
        if self.winning_trades == 0:
            return 0
        else:
            self.average_time_in_winning_trade = overall_time / self.winning_trades
            return self.average_time_in_winning_trade

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
        if self.losing_trades == 0:
            return 0
        else:
            self.average_time_in_losing_trade = overall_time / self.losing_trades
            return self.average_time_in_losing_trade

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
        if cons_winners:
            self.max_consecutive_winners = max(cons_winners)
            return self.max_consecutive_winners
        else:
            return 0

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
        if cons_losses:
            self.max_consecutive_losers = max(cons_losses)
            return self.max_consecutive_losers
        else:
            return 0

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

    def _do_all_caclulations(self):
        if not self.all_positions_:
            print("No backtest statistics available!")
            return
        all_stats = [method for method in dir(BacktestStatistics) \
                            if callable(getattr(BacktestStatistics, method)) \
                            if method.startswith('calculate_')]
        for method in all_stats:
            eval("self." + method)()

    def backtest_results(self, plot = True):
        if not self._calculated:
            self._do_all_caclulations()
            self._calculated = 1
        if plot and self.all_positions_:
            plot_cs_prof(self.alg)
            html = "<table>"
            for elem in self.__dict__:
                if elem[-1] == "_" or elem[0] == "_":
                    continue
                value = eval("self." + elem)
                #if type(value) is int or type(value) is float or type(value)
                if type(value) in (int, float, np.float64):
                    html += "<tr><td>" + elem + "</td><td>" + str(
                        value) + "</td></tr>"
            html += "</table>"
            with open("stats.html", "r") as file:
                filedata = file.read()
            filedata.replace("</body>", "")
            filedata.replace("</html>", "")
            with open("stats.html", "a") as file:
                file.write(html)
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', "stats.html"))
            elif os.name == 'nt':
                os.startfile("stats.html")
            elif os.name == 'posix':
                subprocess.call(('xdg-open', "stats.html"))

