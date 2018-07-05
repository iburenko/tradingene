class TimeEvent:
    def __init__(self, ticker=None, time=None, handler=None):
        self._ticker = ticker
        self._time = time
        self._handler = handler
        self._id = 0

    @classmethod
    def check(cls, obj):
        expired = [event for event in obj.time_events \
                              if obj.now >= obj.time_events.time]
        for event in expired:
            event.handler()
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
        if self.time == other.time and self.handler == other.handler:
            eq = True
        return True

    def __str__(self):
        print("TIME EVENT IS PRINTING!!!!")
        for key, value in self.__dict__.items():
            print(key, value)
        return ""
