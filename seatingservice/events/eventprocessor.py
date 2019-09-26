from events.seatrequestevent import SeatRequestEvent
from events.exceptions import InvalidEventException

from utils.logs import Logger

logging = Logger.get_logger()


class SeatAssigner:

    def __init__(self, seats_assigninig_service, event_consumer, event_producer):
        self.assign_service = seats_assigninig_service
        self.consumer = event_consumer  # can have a wrapped consumer to be always in consistent with what is expected
        self.event_producer = event_producer

    def process(self):
        for event in self.consumer:
            try:
                logging.info("Received Event {}".format(str(event)))
                event_obj = SeatRequestEvent.validate_event(event)
                response = self.assign_service.post(request_params=event_obj.to_dict())
                print(response)
                if response.get("status") == "success":
                    response_string = " ".join(response.get("seats"))
                    self.event_producer.write("{} {}\n".format(event_obj.get_txn_id(), response_string))
                    logging.info("Assigned Seats {} {}".format(str(event_obj.get_txn_id()), response.get("body")))
                else:
                    logging.error("Could not assign to request event_obj {}".format(event_obj.to_dict()))
                    self.event_producer.write("{}\n".format(event_obj.get_txn_id()))
            except InvalidEventException as e:
                """Uncomment to allow the invalid data to be written to file"""
                # self.event_producer.write("{} {}\n".format(event.strip("\n"), "Invalid Request data"))
                logging.error("Invalid event_obj {} exception {}".format(str(event).strip("\n"), e))
