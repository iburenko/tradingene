from datetime import datetime
from tng.algorithm_backtest.trade_activity import TradeActivity


class TNG(TradeActivity):
    """ TNG class contains all needed functionality for backtesting.

        If you want to create an instance of the TNG class
        you must specify date of the start of backtest
        and the date of the end of backtest.
        You may explicitly specify the name of your algorithm
        and the backtest regime. If you do not specify these
        arguments default values will be used.

        Arguments:
            name (str, optional): Name of the algorithm.
                Default value is "Cornucopia".
            regime (str, optional): Controls number of trades
                in a single position. In "SP" regime only one trade is
                allowed, in "MP" multiple trades are allowed.
            start_date (datetime.datetime): Start time of the backtest.
            end_date (datetime.datetime): End time of the backtest.            

        Examples:
            ```python
                # Constructor with only two parameters.
                # Default values for name and regime will be used.
                # default name is "Cornucopia",
                # default regime is "SP" (single position).
                # Note: start_date and end_date may be specified
                # in any order.
                from datetime import datetime
                from tng.algorithmic_backtest.tng import TNG
                start_date = datetime(2018, 1, 1)
                end_date = datetime(2018, 2, 1)
                alg = TNG(start_date, end_date)
            ```
            ```python
                # Constructor with three parameters:
                # name, start_date, end_date;
                # by default regime is "SP".
                # Note: start_date and end_date may be specified
                # in any order
                from datetime import datetime
                from tng.algorithmic_backtest.tng import TNG
                name = "Fleece"
                start_date = datetime(2018, 1, 1)
                end_date = datetime(2018, 2, 1)
                alg = TNG(name, start_date, end_date)
            ```
            ```python
                # Constructor with three parameters:
                # regime, start_date, end_date;
                # by default name is "Cornucopia".
                # Note: start_date and end_date may be specified
                # in any order.
                from datetime import datetime
                from tng.algorithmic_backtest.tng import TNG
                regime = "MP"
                start_date = datetime(2018, 1, 1)
                end_date = datetime(2018, 2, 1)
                alg = TNG(name, start_date, end_date)
            ```python
                # Constructor with four parametera:
                # name, regime, start_date, end_date
                # Note: name must be specified before regime,
                # after name and regime start_date, end_date 
                # may be specified in any order.
                name = "Fleece"
                regime = "MP"
                start_date = datetime(2018, 1, 1)
                end_date = datetime(2018, 2, 1)
                alg = TNG(name, regime, start_date, end_date)
            ```

        Raises:
            ValueError: If four variables sent to the constructor
                but not in the following order: 
                (name, regime, start_date, end_date)
            ValueError: If more than two string variables sent 
                to the constructor
            ValueError: If regime is not "SP" or "MP"
            ValueError: If constructor receives more that 
                two string variables
            ValueError: If construcotr receives any number
                different from two datetime variables
            ValueError: If start_date coincides with end_date
    """

    def __init__(self, *args):
        try:
            assert len(args) == 4
            name, regime = args[0], args[1]
            start_date, end_date = args[2], args[3]
            if regime != "SP" and regime != "MP":
                err_str = "regime cannot be {}! ".format(regime)+\
                          "Regime must be ''SP'' or ''MP'' "
                raise ValueError(err_str)
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
