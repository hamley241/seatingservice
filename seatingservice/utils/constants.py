from enum import Enum

class SeatsRequest:
    TXN_ID = "txnId"
    NUM_SEATS = "seatsCount"
    SEATS = "seats"


class SeatsResponse:
    STATUS = "status"
    SEATS = "seats"


class ResponseStatusCode(Enum):
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    INTERNAL_ERROR = 500

class SeatStatus(Enum):
    BOOKED = 1
    NOT_BOOKED = 0
    BLOCKED = 2 # In cart
    ON_HOLD = 3 # MAY BE SOME ISSUE -LIKE SEATS DAMAGED FOR NOW


    @classmethod
    def is_valid(cls, seat_status):
        if seat_status in [cls.NOT_BOOKED, cls.BOOKED, cls.BLOCKED, cls.ON_HOLD]:
            return True
        return False

class SeatType(Enum):
    NORMAL = 1
    EXECUTIVE = 0
    RECLYNER = 2 #

    @classmethod
    def is_valid(cls, seat_type):
        if seat_type in [cls.NORMAL, cls.EXECUTIVE, cls.RECLYNER]:
            return True
        return False

