import logging
import time
import app.views as views

class Seats(object):
    def post(self, request_params):
        txn_id = request_params.get("txnId")
        no_seats =  request_params.get("SeatsCount")

        if not txn_id or not no_seats:
            return views.get_failed_response({"txnId":txn_id}) #400 response

        ## Call models to assign actual seats

        models.theatre.assign(txn_id, no_seats)