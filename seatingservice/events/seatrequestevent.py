from events.exceptions import InvalidEventException
from utils import validate_int
from utils.logs import Logger

logging = Logger.get_logger(__name__)


class SeatRequestEvent:
    """
    SeatRequest event
    """

    def __init__(self, trxn_id, seats_count):
        self._txn_id = trxn_id
        self._seats_count = seats_count

    def get_txn_id(self):
        return self._txn_id

    def get_seats_count(self):
        return self._seats_count

    def to_dict(self):
        """
        Returns: The event data in form of dict
        """
        return dict(txnId=self.get_txn_id(), seatsCount=self.get_seats_count())

    @classmethod
    def validate_event(cls, event):
        """
        Validates the possible event string and returns event object
        Args:
            event: string containig event data

        Returns: SeatRequestEvent

        """
        if not event:
            logging.debug("No event")
            raise InvalidEventException()

        data = event.rstrip("\n").rstrip("\r").rstrip("\n").strip(" ").split(" ")
        if not data:
            logging.debug("Data is None or Empty")
            raise InvalidEventException()

        if data and not len(data) == 2:
            logging.debug("Length of data != 2, event is {} and length is {}, data is {}".format(event, str(len(data)),str(data)))
            raise InvalidEventException()

        txn_id = data[0]
        try:
            seats_count = validate_int(data[1])
        except Exception as e:
            logging.debug("Seats count is not int, event is {}".format(event))
            raise InvalidEventException

        if not txn_id.startswith("R"):
            logging.debug("Does not start with R, event is {}".format(event))
            raise InvalidEventException()

        try:
            validate_int(txn_id[1:])
        except Exception as e:
            logging.debug("Issue with TransactionID event is {}".format(event))
            raise InvalidEventException()

        return SeatRequestEvent(txn_id, seats_count)
