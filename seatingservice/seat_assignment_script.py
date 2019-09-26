import sys
import os
from app.controllers import Seats
import argparse

import datetime
from utils.logs import Logger

logging = Logger.get_logger()


class InvalidEventException(Exception):
    pass


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


class SeatAssigner:

    def __init__(self, seats_asssginig_service, event_consumer, event_producer):
        self.assign_service = seats_asssginig_service
        self.consumer = event_consumer  # can have a wrapped consumer to be always in consistent with what is expected
        self.event_producer = event_producer

    def process(self):
        for event in self.consumer:
            try:
                logging.info(" {} Received Event {}".format(datetime.datetime.utcnow(), str(event)))
                event = self.validate_event(event)
                response = self.assign_service.post(request_params=event.to_dict())
                if response.get("status") == "success":
                    self.event_producer.write("{}\n".format(response.get("body")))
                else:
                    logging.error("No seat was assigned to request event {}".format(event.to_dict()))
            except InvalidEventException as e:
                logging.error("Invalid event {} exception {}".format(str(event).strip("\n"), e))
            print("Result")

    def validate_event(self, event):
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

        return SeatRequestEvent(txn_id, seats_count)


if __name__ == "__main__":
    help_text = "seat_assignment_script.py: error: the following arguments are required: inputfile \n ex: {} inputfile.txt".format(
                "seat_assignment_script.py")
    if len(sys.argv) != 2:
        print(help_text)
        os._exit(1)

    if not os.path.isfile(sys.argv[1]):
        logging.error("Requires a file path\n{}".format(help_text))
        os._exit(1)
    inputfile = sys.argv[1]
    requests_file = open(inputfile, "r")
    response_file_name = "responses.txt"
    response_file = open(response_file_name, "w")
    seats_asssginig_service = Seats()
    seat_assigner = SeatAssigner(seats_asssginig_service, requests_file, response_file)
    seat_assigner.process()
    print("Responses can be found at {}".format(os.path.abspath(response_file_name)))
