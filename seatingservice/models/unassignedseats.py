from models.seatorderdict import SeatOrderDict


class UnavailableSeats(SeatOrderDict):

    def __setitem__(self, key, value):
        if not isinstance(value, dict):
            raise TypeError("Expecting object of type {}".format(dict.__name__))
        super().__setitem__(key, value)

    def add_row(self, key, seats_row):
        if not isinstance(seats_row, dict):
            raise TypeError()
        self.__setitem__(key, seats_row)

    def has(self, seat_number):
        row_num, col_num = self._get_row_col_numbers(seat_number)
        seat_obj = col_num in self.get(row_num, dict())
        if not seat_obj:
            return False
        return True

    def add(self, complete_seat_number, txn_id=None):
        row, col = self._get_row_col_numbers(complete_seat_number)
        try:
            self.get_row(row).__setitem__(col, txn_id)
        except KeyError as e:
            self.add_row(row, dict())
            self.get_row(row).__setitem__(col, txn_id)

    def __str__(self):
        response_str = ""
        for row, seats_row in self.items():
            response_str = "{}\n{}".format(response_str, " ".join([str(row) + str(item) for item in seats_row]))
        return response_str
