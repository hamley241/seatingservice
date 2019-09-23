from enum import Enum

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

