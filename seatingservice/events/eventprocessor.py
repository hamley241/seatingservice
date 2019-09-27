from events.seatrequestevent import SeatRequestEvent
from events.exceptions import InvalidEventException

from utils.logs import Logger
from utils.constants import SeatsResponse

logging = Logger.get_logger()


class SeatAssigner:
    """
    This is a Event Processor can be extended to process multiple events using match methods and process methods them being called on process here
    """

    def __init__(self, seats_assigninig_service, event_consumer, event_producer):
        self.assign_service = seats_assigninig_service
        self.consumer = event_consumer  # can have a wrapped consumer to be always in consistent with what is expected
        self.event_producer = event_producer  # Can also be a Kafka Like service where post ticket booking we can send SMS, Updates and stuff related to that

    def process(self):
        """
        This function process the events that come from the event producer.
        Returns: None

        """
        for event in self.consumer:
            try:
                logging.info("Received Event {}".format(str(event)))
                event_obj = SeatRequestEvent.validate_event(event)  # Parsing, validating  and getting event object

                response = self.assign_service.post(request_params=event_obj.to_dict())  # Request to seats service

                if response.get(SeatsResponse.STATUS) == "success":
                    # Request was processed by service successfully
                    response_string = ",".join(response.get(SeatsResponse.SEATS))
                    self.event_producer.write("{} {}\n".format(event_obj.get_txn_id(), response_string))
                    logging.info("Assigned Seats {} {}".format(str(event_obj.get_txn_id()), response_string))
                else:
                    # Request failed
                    logging.error("Could not assign to request event_obj {}".format(event_obj.to_dict()))
                    self.event_producer.write("{}\n".format(event_obj.get_txn_id()))
            except InvalidEventException as e:
                # Malformed events go here
                """Uncomment to allow the invalid data to be written to file"""
                # self.event_producer.write("{} {}\n".format(event.strip("\n"), "Invalid Request data"))
                logging.error("Invalid event_obj {} exception {}".format(str(event).strip("\n"), e))
