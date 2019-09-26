from models.seatorderdict import SeatOrderDict
from models.exceptions import SeatNotFoundException
from models.seatsrow import SeatsRow


class ScreenLayout(SeatOrderDict):

    def add_row(self, key, seats_row):
        if not isinstance(seats_row, SeatsRow):
            raise TypeError()
        self.__setitem__(key, seats_row)

    def find(self, seat_number):
        row_num, col_num = self._get_row_col_numbers(seat_number)
        seat_obj = self.get(row_num, {}).get(col_num)
        if not seat_obj:
            raise SeatNotFoundException()
        return seat_obj

    def __setitem__(self, key, value):
        if not isinstance(value, SeatsRow):
            raise TypeError("Expecting object of type {}".format(SeatsRow.__name__))
        super().__setitem__(key, value)
