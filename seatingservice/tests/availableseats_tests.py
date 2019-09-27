import unittest
from models.availableseats import AvailableSeats


class TestAvailableSeats(unittest.TestCase):
    def setUp(self):
        self.obj = AvailableSeats()

    def test_add_row(self):
        # If object is not of set type
        test_row = {2, 3}
        test_key = "A"
        self.assertRaises(TypeError, self.obj.add_row, test_key, dict())

        ##No exception if object is Same item is retrieved
        self.obj.add_row(test_key, test_row)
        assert test_row == self.obj.pop(test_key)

    def test_has(self):
        test_row = {2, 3}
        test_key = "A"
        self.obj.add_row(test_key, test_row)
        assert self.obj.has("A2") == True
        assert self.obj.has("A3") == True
        assert self.obj.has("A4") == False

    def test_add(self):
        self.obj.add("B1")
        assert self.obj.has("B1") == True


    def test___str__(self):
        test_row = {2, 3}
        test_key = "A"
        self.obj.add_row(test_key, test_row)
        assert self.obj.__str__().strip("\n") == "A2 A3"
        assert str(self.obj) != "A$ A3"

if __name__ == '__main__':
    unittest.main()
