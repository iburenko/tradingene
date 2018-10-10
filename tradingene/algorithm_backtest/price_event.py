class PriceEvent:
    def __init__(self, \
                 ticker = None, price = None, trigger = None, \
                 arguments = None, handler = None):
        """ Handles callbackes on a given price.

        Arguments:
            ticker (str): See attributes.
            price (float): See attributes.
            trigger (int): See attributes.
            handler (function): See attributes.
            
        
        Attributes:
            ticker (str): Name of an asset.
            price (): Time stamp. At the moment when backtest will reach
                specified time stamp callaback will invoke.
            trigger (int): Indicates whether from below or from above current
                price need to strike specified:
                    a) trigger = 1, if current price at the moment of setting
                        price event was below strike price;
                    b) trigger = -1, otherwise.
            handler (function): Callback that is called when current price
                strikes the specified price.

        Raises:
            TypeError: If handler is not callable.
    """

        self._ticker = ticker
        self._threshold = price
        self._trigger = trigger
        self.arguments = arguments
        self._handler = handler

    @classmethod
    def check(cls, obj):
        """ Checks whether any price event should be handled

            Attributes:
                obj (TNG): TNG class instance that contains all price events
                    if any.

            Returns:
                None
        """
        expired = [event for event in obj.price_events\
                if (event.threshold - obj.recent_price)*event.trigger <= 0]
        for event in expired:
            obj.recent_price = (event.threshold, 0)
            event.handler(event.arguments)
            obj.price_events.remove(event)


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
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = value

    @threshold.deleter
    def threshold(self):
        self._threshold = None

    @property
    def trigger(self):
        return self._trigger

    @trigger.setter
    def trigger(self, value):
        self._trigger = value

    @trigger.deleter
    def trigger(self):
        self._trigger = 0

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
        if self.threshold == other.threshold:
            if self.trigger == other.trigger:
                if self.handler == other.handler:
                    eq = True
        return eq
