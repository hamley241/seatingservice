import logging
from utils.constants import SeatStatus, SeatType


class Seat(object):

    def __init__(self, col_num, row_num,status=SeatStatus.NOT_BOOKED,seat_type = SeatType.NORMAL):
        self._row_num = row_num
        self._col_num = col_num
        self._status = status
        self.seat_type = seat_type


    def __str__(self):
        return "".join([str(self._col_num), str(self._row_num)])

    def get_name(self):
        return "".join([str(self._col_num), str(self._row_num)])

    def book(self):
        if self.is_booked():
            return False
        return self._book()


    # Can take a lock here based on whatever database we are gonna use
    def _book(self):
        if self.get_status() == SeatStatus.NOT_BOOKED:
            return self._set_status(SeatStatus.BOOKED)
        return False


    def is_booked(self):
        return SeatStatus.BOOKED == self.get_status()

    def is_empty(self):
        return SeatStatus.NOT_BOOKED == self.get_status()


    def get_status(self):
        return self._status

    def _set_status(self, booking_status):
        if not SeatStatus.is_valid(booking_status):
            return False # Can raise exception
        self._status = booking_status
        return True


if __name__ == "__main__":
    seat = Seat("A",1)
    print(seat)
    print(seat.get_status())
    if seat.book():
        print("Seat booked successfully")
    else:
        print("Issue booking the seat")
    print("Booking already booked seat {} {} ".format(str(seat.book()), "2"))
