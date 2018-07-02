from tng.algorithm_backtest.trade_activity import TradeActivity
from datetime import datetime


class TNG(TradeActivity):
    def __init__(self, *args):
        try:
            assert len(args) == 4
            name, regime = args[0], args[1]
            start_date, end_date = args[2], args[3]
            if isinstance(name, str) and \
                isinstance(regime, str) and \
                isinstance(start_date, datetime) and \
                isinstance(end_date, datetime):
                super(TNG, self).__init__(name, regime, start_date, end_date)
            else:
                raise ValueError(
                    "Input variables is not (str, str, datetime, datetime) tuple!"
                )

        except AssertionError:
            string_vars = [
                str_var for str_var in args if isinstance(str_var, str)
            ]
            datetime_vars = [
                dtm_var for dtm_var in args if isinstance(dtm_var, datetime)
            ]
            if len(string_vars) > 2:
                raise ValueError(
                    "In TNG(...) there are only two string variables allowed! Check the constructor!"
                )
            if len(datetime_vars) != 2:
                raise ValueError(
                    "In TNG(...) there must be two datetime variables allowed! Check the constructor!"
                )
            start_date = min(datetime_vars)
            end_date = max(datetime_vars)
            if start_date == end_date:
                raise ValueError(
                    "The start date cannot be equal to the end date!")
            if len(string_vars) == 0:
                name = "Cornucopia"
                regime = "SP"
            elif len(string_vars) == 1:
                if string_vars[0] == "SP" or string_vars[0] == "MP":
                    name = "Cornucopia"
                    regime = string_vars[0]
                else:
                    name = string_vars[0]
                    regime = "SP"
            else:
                name = string_vars[0]
                if string_vars[1] == "SP" or string_vars[1] == "MP":
                    regime = string_vars[1]
                else:
                    raise ValueError("Regime must be ''SP'' or ''MP'' ")
            super(TNG, self).__init__(name, regime, start_date, end_date)
