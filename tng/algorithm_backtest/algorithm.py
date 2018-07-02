class Algorithm:
    """ Base class for algorithm

        In the initialization step you may specify:

        # 1. Name of your algorithm, by default set to empty string
        # 2. Regime of backtest. By default it is set to "SP"
             ("single position"), other possibility is "MP"
             ("multiple position").
             The former means that you are able to operate with only one lot
             in algorithm logic, while the last means that you are able to
             operate with multiple positions in your algorithm but total
             volume available is still 1.

        If you'll try to delete attribute value it'll be set to default value
    """

    def __init__(self, name="", regime="SP"):
        self._name = name
        self._regime = regime

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert type(value) is str
        self._name = value

    @name.deleter
    def name(self):
        self._name = ""

    @property
    def regime(self):
        return self._regime

    @regime.setter
    def regime(self, value):
        assert value == "SP" or value == "MP"
        self._regime = value

    @regime.deleter
    def regime(self):
        self._regime = "SP"
