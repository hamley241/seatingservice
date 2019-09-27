import unittest
from models.seat import Seat

class TestSeat(unittest.TestCase):

    def setUp(self):
        self.seat_class = Seat

    def test_create(self):
        assert "A1" == self.seat_class.get_seat_name("A",1)


if __name__ == '__main__':
    unittest.main()
