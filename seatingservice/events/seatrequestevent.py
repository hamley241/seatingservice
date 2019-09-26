from events.exceptions import InvalidEventException
from utils import validate_int


class SeatRequestEvent:

    def __init__(self, trxn_id, seats_count):
        self._txn_id = trxn_id
        self._seats_count = seats_count

    def get_txn_id(self):
        return self._txn_id

    def get_seats_count(self):
        return self._seats_count

    def to_dict(self):
        return dict(txnId=self.get_txn_id(), seatsCount=self.get_seats_count())

    @classmethod
    def validate_event(cls, event):
        if not event:
            raise InvalidEventException()

        data = event.strip("\n").split(" ")
        if not len(data) == 2:
            raise InvalidEventException()

        txn_id = data[0]
        try:
            seats_count = int(data[1])
        except Exception as e:
            raise InvalidEventException

        if not txn_id.startswith("R"):
            raise InvalidEventException()

        try:
            validate_int(txn_id[1:])
        except Exception as e:
            raise InvalidEventException()

        return SeatRequestEvent(txn_id, seats_count)
