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
        data_dict[self.row] = self._serialize_value()
        return True


    def _serialize_value(self):
        return {STATUS: self._status, SEAT_TYPE: self._seat_type}

    @classmethod
    def _deserialize(cls, obj_data):
        pass
