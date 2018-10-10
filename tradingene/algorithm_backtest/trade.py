from numpy import sign


class Trade:
    """ Contains information about one particular trade. 

        Arguments:
            id (int): See attributes.
            open_price (float): See attributes.
            close_price (float): See attributes.
            volume (float): See attributes.
            side (int): See attributes.
            open_time (int): See attributes.
            close_time (int): See attributes.
    
        Attributes:
            id (int): id of the trade. The first trade has
                random int. The next trade in the position
                has id increased by one. Trade in the next
                position has random int id again.
            open_price (float): open price of the trade.
            close_price (float): close_price of the trade.
            volume (float): volume of the trade.
            side (int): if the trade was long then side is 1,
                if the trade was short then the side is -1.
            open_time (int): time at which the trade was open.
            close_time(int): time at which the trade was closed,
                if MP regime is used for all trades will be used
                the time at which position was close.
                If trade is not closed, then close_time is 0.
    """

    def __init__(self, id_, open_price, volume, open_time):
        self.id = id_
        self.open_price = open_price
        self.close_price = 0
        self.volume = volume
        self.side = sign(volume)
        self.open_time = open_time
        self.close_time = 0
