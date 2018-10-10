class TimeEvent:
    """ Handles callbackes on a given time.

        Arguments:
            ticker (str): See attributes.
            time (int): See attributes.
            handler (function): See attributes.
            
        
        Attributes:
            ticker (str): Name of an asset.
            time (int): Time stamp. At the moment when backtest will reach
                specified time stamp callaback will invoke.
            handler (function): Callback that is called when current backtest
                time reaches specified time or exceeds it.

        Raises:
            TypeError: If handler is not callable.
    """

    def __init__(self, ticker=None, time=None, arguments=None, handler=None):
        self._ticker = ticker
        self._time = time
        self.arguments = arguments
        self._handler = handler

    @classmethod
    def check(cls, obj):
        """ Checks whether any time event should be handled

            Attributes:
                obj (TNG): TNG class instance that contains all time events
                    if any.

            Returns:
                None
        """
        expired = [event for event in obj.time_events \
                              if obj.now >= obj.time_events.time]
        for event in expired:
            event.handler(event.arguments)
            obj.time_events.remove(event)


################################################################################

    @property
    def ticker(self):
        return self._ticker

    @ticker.setter
    def ticker(self, value):
        self._ticker = value

    @ticker.deleter
    def ticker(self):
        self._ticker = ""

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @time.deleter
    def time(self):
        self._time = None

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, value):
        if callable(value):
            self._handler = value
        else:
            raise TypeError("Handler must be callable!")

    @handler.deleter
    def handler(self):
        self._handler = None

    def __eq__(self, other):
        eq = False
        if self.now == other.now and self.handler == other.handler:
            eq = True
        return True
