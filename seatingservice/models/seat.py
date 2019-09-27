import logging
from utils.constants import SeatType


class Seat(object):
    """
    A Basic seat object with its attributes, to enable creation of seats and utils around them
    """
    def __init__(self, row, col, seats_type=SeatType.NORMAL, metadata={}):
        self._row = self.validate_row(row)
        self._col = self.validate_col(col)
        self._seats_type = self.validate_seats_type(seats_type)
        self._metadata = metadata

    def get_row(self):
        return self._row

    def get_col(self):
        return self._col

    def get_seats_type(self):
        return self._seats_type

    def get_metedata(self):
        return self._metadata

    @staticmethod
    def validate_row( row):
        if not isinstance(row, str):
            logging.error("validate_row  Expecting a string got {}".format(type(row)))
            raise TypeError("Expecting String got {}".format(type(row)))

        if row.strip() == "":
            logging.error("validate_row  Expecting a valued string got empty string")
            raise ValueError("Expecting a valued string got empty string")
        return row.strip(" ")

    @staticmethod
    def validate_col(col):
        if not isinstance(col, int):
            try:
                col = int(col.strip())
            except Exception as e:
                logging.error("validate_col  Expecting a string got {}".format(type(col)))
                raise TypeError("Expecting int got {}".format(type(col)))

        if col < 0:
            logging.error("validate_col  Expecting a valued string got empty string")
            raise ValueError("Expecting a valued string got empty string")
        return col

    def __str__(self):
        return "".join([self.get_row(), str(self.get_col())])

    @staticmethod
    def validate_seats_type(seat_type):
        if not isinstance(seat_type, SeatType):
            logging.error("validate_seats_type  Expecting a SeatType input got {}".format(type(seat_type)))
            raise TypeError("Expecting validate_seats_type got {}".format(type(seat_type)))

        if not SeatType.is_valid(seat_type):
            logging.error("validate_seats_type  expecting a valid SeatType ")
            raise ValueError("Expecting a valid input SeatType")
        return seat_type

    @staticmethod
    def get_seat_name(row, col):
        return "".join([row, str(col)])
