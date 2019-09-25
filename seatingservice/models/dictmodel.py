from utils.constants import SeatStatus, SeatType
from collections import OrderedDict

from abc import ABC, abstractmethod


class DictModelException(Exception):
    pass


class DataNotFoundException(DictModelException):
    pass


class InvalidDataException(DictModelException):
    pass


class DataCorruptedException(DictModelException):
    # This is a CRITICAL EXCEPTION, We should let the application fail
    pass


STATUS = "status"
SEAT_TYPE = "type"


class DictModel(ABC):
    _datastore = None

    @classmethod
    def _get_class_dict(cls):
        if not cls._datastore:
            cls.init_database()
        return cls._datastore

    @classmethod
    def init_database(cls):
        if cls._datastore is None:
            cls._datastore = OrderedDict()

    @classmethod
    def _find(cls, primary_key):
        return cls._get_class_dict().get(primary_key, {})

    @classmethod
    @abstractmethod
    def find(cls, search_key):
        pass

    @abstractmethod
    def save(self):
        pass

    @classmethod
    @abstractmethod
    def _deserialize(cls, obj_data):
        pass


class SeatModel(DictModel):

    def __init__(self, col):
        self._col = col
        self._status = None
        self._seat_type = None

    def get_col(self):
        return self._col

    def get_status(self):
        return self._status

    def set_status(self, status):
        if not SeatStatus.is_valid(status):
            raise InvalidDataException()
        self._status = status
        return

    def get_seat_type(self):
        return self._seat_type

    def set_seat_type(self, seat_type):
        if not SeatType.is_valid(seat_type):
            raise InvalidDataException()
        self._seat_type = seat_type

    def save(self):
        self.__class__.init_database()
        data_dict = self.__class__._get_class_dict()
        data_dict[self._col] = self._serialize_value()
        return True

    def _serialize_value(self):
        return {STATUS: self._status, SEAT_TYPE: self._seat_type}

    def to_dict(self):
        return {self.get_col(): self._serialize_value()}

    @classmethod
    def _deserialize(cls, obj_data):
        col_name = list(obj_data.keys())[0]
        status = obj_data[col_name].get(STATUS)
        seat_type = obj_data[col_name].get(SEAT_TYPE)
        try:
            seat_obj = SeatModel(col=col_name)
            seat_obj.set_seat_type(seat_type)
            seat_obj.set_status(status)
        except InvalidDataException as e:
            raise DataCorruptedException()
        return seat_obj

    def __str__(self):
        return str(self.get_col())

    @classmethod
    def find(cls, col):
        obj_data = cls._find(col)
        if not obj_data:
            raise DataNotFoundException()
        return cls._deserialize({col: obj_data})


class SeatsRow1(OrderedDict):

    def find(cls, search_key):
        obj_data = cls._find(search_key)
        if not obj_data:
            raise DataNotFoundException()
        return cls._deserialize({search_key: obj_data})

    def save(self):
        self.__class__.init_database()
        data_dict = self.__class__._get_class_dict()
        data_dict[self.row] = self._serialize_value()
        return True


    def _serialize_value(self):
        return {STATUS: self._status, SEAT_TYPE: self._seat_type}

    @classmethod
    def _deserialize(cls, obj_data):
        pass

"""

"""
class SeatNotFoundException(Exception):
    pass

import re


class SeatOrderDict(OrderedDict):
    def _get_row_col_numbers(self, seat_number):
        col_number = re.findall('\d+', seat_number)[0]
        row_number = seat_number.replace(col_number,"")
        print(str(row_number)+" row")
        print(str(col_number)+" col")
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

    def _get_row_col_numbers(self, seat_number):
        col_number = re.findall('\d+', seat_number)[0]
        row_number = seat_number.replace(col_number,"")
        print(str(row_number)+" row")
        print(str(col_number)+" col")
        return row_number,col_number


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

class SeatsRow(OrderedDict):

    def find(self, col_num):
        return self.get(col_num)

    def __setitem__(self, key, value):
        if not isinstance(value, VanillaSeat):
            raise TypeError("Expecting object of type {}".format(VanillaSeat.__name__))
        super().__setitem__(key, value)

    def add_seat(self, key, value):
        self.__setitem__(str(key),value)

    def __str__(self):
        return " ".join([str(seat) for seat_col, seat in self.items()])


class Screen(object):
    #TODO : Make this immutable
    def __init__(self, layout_config, name="default"):
        self._name = name
        self._layout = ScreenLayout()
        seats_conf = layout_config.get(self._name).get("seats_matrix")
        self._init_layout(seats_conf)
        self._seats_not_available = NASeats()
        self._init_seats_not_available(seats_conf)
        self._total_seats = self.get_layout().get_total_size()


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
            new_seat = VanillaSeat(row_name, str(col))
            seats_row.add_seat(str(col), new_seat)
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
        return self.get_total_seats() - self.get_not_available_seats().get_total_size()

    def get_total_seats(self):
        return self._total_seats

    def get_layout(self):
        return self._layout

    def _create_na_row(self, row_config):
        return set()


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
        if not isinstance(col, str):
            logging.error("validate_col  Expecting a string got {}".format(type(col)))
            raise TypeError("Expecting String got {}".format(type(col)))

        if col.strip() == "":
            logging.error("validate_col  Expecting a valued string got empty string")
            raise ValueError("Expecting a valued string got empty string")
        return col.strip(" ")

    def __str__(self):
        return "".join([self.get_row(), self.get_col()])

    def validate_seats_type(self, seat_type):
        if not isinstance(seat_type, SeatType):
            logging.error("validate_seats_type  Expecting a SeatType input got {}".format(type(seat_type)))
            raise TypeError("Expecting validate_seats_type got {}".format(type(seat_type)))

        if not SeatType.is_valid(seat_type):
            logging.error("validate_seats_type  expecting a valid SeatType ")
            raise ValueError("Expecting a valid input SeatType")
        return seat_type

if __name__ == "###1__main__":
    sm = SeatModel(2)
    print(sm)
    print(sm.set_status(SeatStatus.NOT_BOOKED))
    print(sm.set_seat_type(SeatType.NORMAL))
    print(sm.save())
    print(sm._datastore)
    cm = SeatModel(3)
    print(cm.set_status(SeatStatus.NOT_BOOKED))
    print(cm.set_seat_type(SeatType.NORMAL))
    print(cm.save())
    print(cm._datastore)

    print(SeatModel.find(2))

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
    print(scr.get_layout().find("A1"))
    print(scr.get_layout())
    print(scr.get_not_available_seats().get_total_size())
