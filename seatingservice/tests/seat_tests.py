import unittest
from models.seat import Seat
from utils.constants import SeatType


class TestSeat(unittest.TestCase):
    acceptable_row = "A"
    acceptable_col = 3

    def setUp(self):
        self.seat_class = Seat

    def test_get_seat_name(self):
        assert "A1" == self.seat_class.get_seat_name("A", 1)

    def test_validate_row(self):
        acceptable_row = "B"
        assert self.seat_class.validate_row(acceptable_row) == acceptable_row
        self.assertRaises(TypeError, self.seat_class.validate_row, 3)
        self.assertRaises(ValueError, self.seat_class.validate_row, "")
        self.assertRaises(ValueError, self.seat_class.validate_row, " ")
        self.assertRaises(TypeError, self.seat_class.validate_row, Seat)

    def test_validate_col(self):
        assert self.seat_class.validate_col(TestSeat.acceptable_col) == TestSeat.acceptable_col
        self.assertRaises(TypeError, self.seat_class.validate_col, Seat)
        self.assertRaises(ValueError, self.seat_class.validate_col, -1)

    def test_validate_seat_type(self):
        assert self.seat_class.validate_seats_type(SeatType.NORMAL) == SeatType.NORMAL
        self.assertRaises(TypeError, self.seat_class.validate_seats_type, "")

    def test_get_row(self):
        acceptable_row = "A"
        acceptable_col = 3
        seat_obj = self.seat_class(acceptable_row, acceptable_col)
        assert seat_obj.get_row() == acceptable_row

    def tear_get_col(self):
        seat_obj = self.seat_class(TestSeat.acceptable_row, TestSeat.acceptable_col)
        assert seat_obj.get_col() == TestSeat.acceptable_col


if __name__ == '__main__':
    unittest.main()
