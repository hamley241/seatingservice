"""

"""

from collections import OrderedDict
from utils.constants import SeatType
from utils import memoize
class SeatNotFoundException(Exception):
    pass

import numpy as np
import re


class SeatOrderDict(OrderedDict):
    def _get_row_col_numbers(self, seat_number):
        col_number = re.findall('\d+', seat_number)[0]
        row_number = seat_number.replace(col_number,"")
        try:
            col_number = int(str(col_number).strip())
        except Exception as e:
            raise ValueError()
        return row_number,col_number

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



class ScreenLayout(SeatOrderDict):


    def add_row(self, key, seats_row):
        if not isinstance(seats_row, SeatsRow):
            raise TypeError()
        self.__setitem__(key, seats_row)

    def find(self, seat_number):
        row_num, col_num = self._get_row_col_numbers(seat_number)
        seat_obj = self.get(row_num,{}).get(col_num)
        if not seat_obj:
            raise SeatNotFoundException()
        return seat_obj




    def __setitem__(self, key, value):
        if not isinstance(value, SeatsRow):
            raise  TypeError("Expecting object of type {}".format(SeatsRow.__name__))
        super().__setitem__(key, value)


class NASeats(SeatOrderDict):

    def __setitem__(self, key, value):
        if not isinstance(value, set):
            raise  TypeError("Expecting object of type {}".format(set.__name__))
        super().__setitem__(key, value)

    def add_row(self, key, seats_row):
        if not isinstance(seats_row, set):
            raise TypeError()
        self.__setitem__(key, seats_row)

    def has(self, seat_number):
        row_num, col_num = self._get_row_col_numbers(seat_number)
        seat_obj =  col_num in self.get(row_num,{})
        if not seat_obj:
            return False
        return True

    def add(self, complete_seat_number):
        row, col = self._get_row_col_numbers(complete_seat_number)
        self.get_row(row).add(col)

    def __str__(self):
        response_str = ""
        for row, seats_row in self.items():
            response_str = "{}\n{}".format(response_str, " ".join([str(row) + str(item) for item in seats_row]))
        return response_str


class EmptySeats(NASeats):
    pass
    # def __str__(self):
    #     response_str = ""
    #     for row, row_data in self.items():
    #         response_str = "{}\n{}\t{}".format(response_str,row," ".join([ item  for item in row_data.keys()]))

class SeatsRow(OrderedDict):

    def find(self, col_num):
        return self.get(col_num)

    def __setitem__(self, key, value):
        if not isinstance(value, VanillaSeat):
            raise TypeError("Expecting object of type {}".format(VanillaSeat.__name__))
        super().__setitem__(key, value)

    def add_seat(self, key, value):
        self.__setitem__(key,value)

    def __str__(self):
        return " ".join([str(seat) for seat_col, seat in self.items()])


class Screen(object):

    def __init__(self, layout_config, name="default"):
        self._name = name
        self._layout = ScreenLayout()
        self._seats_not_available = NASeats()
        seats_conf = layout_config.get(self._name).get("seats_matrix")
        self._init_layout(seats_conf)
        self._init_seats_not_available(seats_conf)
        self._total_seats_count = self.get_layout().get_total_size()


    def _init_layout(self, layout_config):
        for cnt,row_config in enumerate(reversed(layout_config)):
            row_name =  row_config.get("name")
            row_seats = self._create_row_seats(row_config)
            self._layout.add_row(row_name, row_seats)
        return


    def _create_row_seats(self, row_config):
        seats_row = SeatsRow()
        row_name = row_config["name"]
        number_of_seats = row_config["count"]
        for col in range(1, number_of_seats + 1):
            new_seat = VanillaSeat(row_name, col)
            seats_row.add_seat(col, new_seat)
        return seats_row
        return seats_row

    def _init_seats_not_available(self, layout_config):
        for row_config in reversed(layout_config):
            row_name =  row_config.get("name")
            empty_row = self._create_na_row(row_config)
            self._seats_not_available.add_row(row_name, empty_row)
        return

    def get_not_available_seats(self):
        return self._seats_not_available

    def get_available_seats(self):
        pass#return self.get_total_seats_count() - self.get_not_available_seats().get_total_size()

    def get_total_seats_count(self):
        return self._total_seats_count

    def get_available_seats_count(self):
        return self.get_total_seats_count() - self.get_not_available_seats().get_total_size()

    def get_layout(self):
        return self._layout

    def _create_na_row(self, row_config):
        return set()

    def find_best_seats(self, num_of_seats):
        empty_seats =  self.get_empty_seats()
        return empty_seats

    def get_empty_seats(self):
        empty_seats = EmptySeats()
        for row, row_seats in self.get_layout().items():
            row_of_empty_seats = row_seats.keys() - self.get_not_available_seats().get_row(row)
            empty_seats.add_row(row, row_of_empty_seats)
        return empty_seats


    def  get_string_hash(self, numpy_arr):
        """
        Computes hash string for a 1D numpy array
        Args:
            numpy_arr: 1D numpy array

        Returns: String

        """
        return "".join([str(int(item)) for item in numpy_arr])

    def test_np(self,empty_seats, num_of_seats):
        import numpy as np
        arr = np.array(list(empty_seats.get("A")))
        print("ARR is "+str(arr))
        self.get_numpy_arr_wth_empty_indicators(arr, empty_seats)
        # arr.sort()

        for row, row_data in empty_seats:


        return arr[[oned]==1]

    def get_numpy_arr_wth_empty_indicators(self, arr, empty_seats):
        zeros_arr = np.zeros(max(arr) + 1)
        zeros_arr[list(empty_seats.get("A"))] = 1

    @memoize
    def _get_empty_canvas(self):
        self.get_layout().get
        pass


# class BookedSeats(OrderedDict)

class ReservedSeats(Screen):
    pass



import logging

class VanillaSeat(object):

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

    def validate_row(self, row):
        if not isinstance(row, str):
            logging.error("validate_row  Expecting a string got {}".format(type(row)))
            raise TypeError("Expecting String got {}".format(type(row)))

        if row.strip() == "":
            logging.error("validate_row  Expecting a valued string got empty string")
            raise ValueError("Expecting a valued string got empty string")
        return row.strip(" ")

    def validate_col(self, col):
        if not isinstance(col, int):
            try:
                col =  int(col.strip())
            except Exception as e:
                logging.error("validate_col  Expecting a string got {}".format(type(col)))
                raise TypeError("Expecting int got {}".format(type(col)))

        if col < 0:
            logging.error("validate_col  Expecting a valued string got empty string")
            raise ValueError("Expecting a valued string got empty string")
        return col

    def __str__(self):
        return "".join([self.get_row(), str(self.get_col())])

    def validate_seats_type(self, seat_type):
        if not isinstance(seat_type, SeatType):
            logging.error("validate_seats_type  Expecting a SeatType input got {}".format(type(seat_type)))
            raise TypeError("Expecting validate_seats_type got {}".format(type(seat_type)))

        if not SeatType.is_valid(seat_type):
            logging.error("validate_seats_type  expecting a valid SeatType ")
            raise ValueError("Expecting a valid input SeatType")
        return seat_type

# if __name__ == "###1__main__":
#     sm = SeatModel(2)
#     print(sm)
#     print(sm.set_status(SeatStatus.NOT_BOOKED))
#     print(sm.set_seat_type(SeatType.NORMAL))
#     print(sm.save())
#     print(sm._datastore)
#     cm = SeatModel(3)
#     print(cm.set_status(SeatStatus.NOT_BOOKED))
#     print(cm.set_seat_type(SeatType.NORMAL))
#     print(cm.save())
#     print(cm._datastore)
#
#     print(SeatModel.find(2))

from collections import Set

class BookedSeats(ScreenLayout):
    pass


from utils.config import  Config
if __name__ == "__main__":
    conf = Config.get_data_map().get("theatre")
    scr = Screen(conf)
    for k, v in scr.get_layout().items():
        for k1, v1 in v.items():
            print(type(v1))
    print(scr.get_layout())
    print(scr.get_layout().find("A1"))
    scr.get_not_available_seats().get_row("A").add(1)
    scr.get_not_available_seats().get_row("B").add(1)
    scr.get_not_available_seats().get_row("A").add(2)
    scr.get_not_available_seats().get_row("A").add(3)
    scr.get_not_available_seats().get_row("A").add(6)
    print(scr.get_not_available_seats().get_total_size())
    print(scr.get_available_seats_count())
    print(scr.get_not_available_seats())
    es = scr.find_best_seats(2)
    print(es.get_total_size())
    print("Done")
    oned = scr.test_np(es)
    oned[oned==1]