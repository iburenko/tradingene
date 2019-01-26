from datetime import datetime
from warnings import warn
from tradingene.algorithm_backtest.algorithm import Algorithm
from tradingene.algorithm_backtest.instrument import Instrument


class Environment(Algorithm):
    """ For handling instruments and timeframes.

        Constructor of this class will invoke by the inherited 
        class Backtest.

        Arguments:
            args (tuple): Tuple of variables that needed for initialization
                of the super class Algorithm.

        Attributes:
            start_date (datetime.datetime): Start time of the backtest.
            end_date (datetime.datetime): End time of the backtest.
            ticker_timeframes (dict): Keys of this dictioanry are tickers
                used by an algorithm, values are list of timeframes 
                that was added by a trader for this particular instrument.

    """

    def __init__(self, *args):
        super(Environment, self).__init__(args[0], args[1])
        self._start_date = args[2]
        self.start_date_int = int(args[2].strftime("%Y%m%d%H%M%S"))
        self._end_date = args[3]
        self.end_date_int = int(args[3].strftime("%Y%m%d%H%M%S"))
        self.ticker_timeframes = dict()
        self.instruments = set()
        self.time_events = list()
        self.price_events = list()

    def addInstrument(self, ticker):
        """ Adds specified instrument to an algorithm.

            Notice that at the moment backtest does
            not support several instruments, so do 
            not add several instruments. Backtest
            procedure won't warn or raise an error
            if you'll add more that one instrument.

            Example:

            '''python
                # Add new instrument to your algorithm
                alg = tng(name, regime, start_date, end_date)
                alg.addInstrument("btcusd")
                # After that piece of code your algorithm has
                # object alg which contains all functionality
                # for backtest and your backtest will run on
                # btcusd.
            '''

            Args:
                ticker (str): Name of the underlying asset.

            Returns:
                None

            Warns:
                Warning is raised if you are trying to add
                an instrument that was already added.
        """

        if ticker not in self.ticker_timeframes:
            self.ticker_timeframes[ticker] = list()
        else:
            warn_str = "Instrument {} cannot be added because {} was already added".format(
                ticker,
                list(self.ticker_timeframes)[0])
            warn(warn_str)

    def deleteInstrument(self, ticker):
        """ Deletes specified instrument from an algorithm.

            Example:

            '''python
                # Add new instrument to your algorithm
                alg = tng(name, regime, start_date, end_date)
                alg.addInstrument("btcusd")
                alg.addInstrument("ethusd")
                alg.deleteInstrument("btcusd")
                # After that piece of code your algorithm
                # will have only one instrument, namely
                # ethusd.
            '''

            Args:
                ticker (str): Name the asset to delete

            Returns:
                None
        """

        if ticker in self.ticker_timeframes:
            del self.ticker_timeframes[ticker]
            self.instruments -= {instr for instr in self.instruments\
                                if instr.ticker == ticker}


    def addTimeframe(self, ticker, *timeframes):
        """ Adds specified timeframes to an algorithm.

            Example:

            '''python
                # Add new instrument to your algorithm
                alg = tng(name, regime, start_date, end_date)
                alg.addInstrument("btcusd")
                alg.addTimeframe("btcusd", 5, 15)
                # After this piece of code your algorithm
                # will add btcusd as the underlying asset
                # and will add 5 and 15 minutes timeframes,
                # what means that user defined on_bar function
                # will invoke after each 5 and 15 minutes candles
                # fully formed.
            '''

            Args:
                timeframes (tuple): Tuple of ints

            Returns:
                None

            Raises:
                TypeError: If tuple has non int element
        """

        for elem in timeframes:
            if not isinstance(elem, int):
                raise TypeError("timeframe must be int")
        if ticker in self.ticker_timeframes:
            existed = set(self.ticker_timeframes[ticker])
            candidates = set(timeframes)
            self.ticker_timeframes[ticker] = sorted(list(existed | candidates))
            ticker_set = {
                Instrument(ticker, timeframe)
                for timeframe in timeframes
            }
            self.instruments |= ticker_set


    def deleteTimeframe(self, ticker, *timeframes):
        """ Deletes specified timeframes from an algorithm.

            Example:

            '''python
                # Add new instrument to your algorithm
                alg = tng(name, regime, start_date, end_date)
                alg.addInstrument("btcusd")
                alg.addTimeframe("btcusd", 5, 15)
                alg.deleteTimeframe("btcusd", 5)
                # After this piece of code your algorithm
                # will add btcusd as the underlying asset
                # and will 15 minutes timeframe,
                # what means that user defined on_bar function
                # will invoke after 15 minutes candles fully formed.
            '''

            Args:
                timeframes (tuple): Tuple of ints

            Returns:
                None

            Raises:
                TypeError: If tuple has non int element
        """

        for elem in timeframes:
            if not isinstance(elem, int):
                raise TypeError("timeframe must be int")
        if ticker in self.ticker_timeframes:
            existed = set(self.ticker_timeframes[ticker])
            candidates = set(timeframes)
            self.ticker_timeframes[ticker] = sorted(list(existed - candidates))
            self.instruments -= {instr for instr in self.instruments\
                                if instr.timeframe in timeframes and
                                   instr.ticker == ticker}


    def getInstrument(self, ticker, timeframe):
        """ Finds specified instruments between existed.

            Example:

            ```python
            # Add two instruments and in onBar get needed one.
            alg = tng(name, regime, start_date, end_date)
            alg.addInstrument("btcusd")
            alg.addTimeframe("btcusd", 5, 15)
            def onBar(instrument):
                if instrument.timeframe == 15:
                    another_instr = alg.getInstrument("btcusd", 5)
            ```

            Args:
                ticker (str): ticker of an instrument
                timeframe (int): timeframe of an instrument

            Returns:
                instr (instrument): if specified instrument was found
                None: else

            Warns:
                warn: If no instrument was found

        """
        
        try:
            assert isinstance(ticker, str)
        except AssertionError:
            warn("In getInstrument ticker must be string!")
        try:
            assert isinstance(ticker, int)
        except AssertionError:
            warn("In getInstrument timeframe must be integer!")
        found = None
        for instr in self.instruments:
            if instr.ticker == ticker and instr.timeframe == timeframe:
                found = instr
        if found is not None:
            return instr
        else:
            warn_str = "In getInstrument there was not instrument with "+\
                        "ticker {} and timeframe = ".format(ticker, timeframe)
            warn(warn_str)
            return None



###############################################################################

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        assert type(value) is datetime
        self._start_date = value
        self.start_date_int = int(value.strftime("%Y%m%d%H%M%S"))

    @start_date.deleter
    def start_date(self):
        self._start_date = None
        self.start_date_int = None

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        assert type(value) is datetime
        today = datetime.today()
        today = datetime(today.year, today.month, today.day)
        if value > today:
            value = today
        self._end_date = value
        self.end_date_int = int(value.strftime("%Y%m%d%H%M%S"))

    @end_date.deleter
    def end_date(self):
        self._end_date = None

    @staticmethod
    def set_start_date(self, value):
        self.start_date = value

    @staticmethod
    def set_end_date(self, value):
        self.end_date = value
