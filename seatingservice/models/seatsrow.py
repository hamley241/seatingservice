from collections import OrderedDict
from models.seat import Seat


class SeatsRow(OrderedDict):

    def find(self, col_num):
        return self.get(col_num)

    def __setitem__(self, key, value):
        if not isinstance(value, Seat):
            raise TypeError("Expecting object of type {}".format(Seat.__name__))
        super().__setitem__(key, value)

    def add_seat(self, key, value):
        self.__setitem__(key, value)

    def __str__(self):
        return " ".join([str(seat) for seat_col, seat in self.items()])
