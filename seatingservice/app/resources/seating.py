import app.views as views
from models.screen import Screen
from utils.config import Config
from utils.constants import SeatsRequest
from utils.logs import Logger
import utils

logging = Logger.get_logger()


class Seats(object):
    _show = Screen(Config.get_data_map().get("theatre"))

    @classmethod
    def post(cls, request_params):
        txn_id = request_params.get(SeatsRequest.TXN_ID, None)
        no_seats = request_params.get(SeatsRequest.NUM_SEATS, None)

        # Data Validation
        if txn_id is None or no_seats is None:
            return views.get_bad_request_response(Seats._get_response_body(txn_id))  # 400 response
        try:
            no_seats = utils.validate_positive_int(no_seats)
        except ValueError as e:
            logging.error("Cleint Error {}".format(str(request_params)))
            return views.get_bad_request_response(Seats._get_response_body(txn_id))

        ## Call models to assign actual seats
        try:
            assigned_seats = cls._show.book(txn_id=txn_id, num_seats=no_seats)
            if not assigned_seats:
                return views.get_failed_response(Seats._get_response_body(txn_id, assigned_seats))
            return views.get_success_response(Seats._get_response_body(txn_id, assigned_seats))
        except Exception as e:
            logging.exception(e)
            return views.get_internal_error_response(Seats._get_response_body(txn_id))  # Internal server error

    @classmethod
    def _get_response_body(cls, txn_id=None, seats=[]):
        response_body = {"txnId": txn_id, "seats": seats}
        return response_body


if __name__ == '__main__':
    print(Seats.post(request_params={"txnId": "RX123", "seatsCount": 3}))
