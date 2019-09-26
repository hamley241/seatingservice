from collections import OrderedDict
import re


class SeatOrderDict(OrderedDict):
    """
    Base DataStructure that will server as Datastore/DB for the Project
    """

    def _get_row_col_numbers(self, seat_number):
        col_number = re.findall('\d+', seat_number)[0]
        row_number = seat_number.replace(col_number, "")
        try:
            col_number = int(str(col_number).strip())
        except Exception as e:
            raise ValueError()
        return row_number, col_number

    def get_total_size(self):
        total_seats = 0
        for row, data in self.items():
            total_seats += len(data)
        return total_seats

    def __str__(self):
        response_str = ""
        for row_name, seats_row in self.items():
            response_str = "{}\n{}".format(response_str, str(seats_row))
        return response_str

    def get_row(self, key):
        return self.__getitem__(key)
