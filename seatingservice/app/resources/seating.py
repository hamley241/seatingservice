import logging
import time
import app.views as views
from models.show import Show

class Seats(object):
    _show = Show()

    @classmethod
    def post(cls, request_params):
        txn_id = request_params.get("txnId")
        no_seats =  request_params.get("seatsCount")

        if not txn_id or not no_seats:

            return views.get_failed_response({"txnId":txn_id}) #400 response

        ## Call models to assign actual seats
        try:
            assigned_seats = cls._show.book(txn_id=txn_id, num_seats=no_seats)
            response_body = "{} {}".format(txn_id, " ".join([seat.get_name() for seat in assigned_seats]))
            return views.get_success_response(dict(body=response_body))
        except Exception  as e:
            print(e.with_traceback())
            return views.get_failed_response({"txnId":txn_id}) #Interal server error



if __name__ == '__main__':
    print(Seats.post(request_params={"txnId":"RX123", "seatsCount":3}))
