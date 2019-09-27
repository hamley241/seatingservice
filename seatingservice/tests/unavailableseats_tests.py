import unittest
from models.unassignedseats import UnavailableSeats


class TestAvailableSeats(unittest.TestCase):
    def setUp(self):
        self.obj = UnavailableSeats()

    def test_add_row(self):
        # If object is not of set type
        test_row = {2: "3"}
        test_key = "A"
        self.assertRaises(TypeError, self.obj.add_row, test_key, set())
        ##No exception if object is Same item is retrieved
        self.obj.add_row(test_key, test_row)
        assert test_row == self.obj.pop(test_key)

    def test_has(self):
        test_row = {2: "3"}
        test_key = "A"
        self.obj.add_row(test_key, test_row)
        assert self.obj.has("A2") == True
        assert self.obj.has("A3") == False
        assert self.obj.has("A4") == False

    def test_add(self):
        self.obj.add("B1","R123")
        assert self.obj.has("B1") == True



if __name__ == '__main__':
    unittest.main()
