from numpy import sign


class Trade:
    def __init__(self, id, open_price, volume, open_time):
        self.id = id
        self.open_price = open_price
        self.close_price = 0
        self.volume = volume
        self.side = sign(volume)
        self.open_time = open_time
