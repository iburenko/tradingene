class PriceEvent:
    def __init__(self, \
                 ticker = None, price = None, trigger = None, handler = None):
        """
        trigger = 1 if the price in the moment of initializing was lower
        than price of an event and -1 otherwise
        """

        self._ticker = ticker
        self._threshold = price
        self._trigger = trigger
        self._handler = handler
        self._id = 0

    @classmethod
    def check(cls, obj):
        expired = [event for event in obj.price_events\
                if (event.threshold - obj.recent_price)*event.trigger < 0]
        for event in expired:
            event.handler()
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

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @id.deleter
    def id(self):
        self._id = 0

    def __eq__(self, other):
        eq = False
        if self.threshold == other.threshold:
            if self.trigger == other.trigger:
                if self.handler == other.handler:
                    eq = True
        return eq

    def __str__(self):
        print("PRICE EVENT IS PRINTING!")
        for key, value in self.__dict__.items():
            print(key, value)
        return ""
