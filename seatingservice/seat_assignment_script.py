import sys
import os
from app.controllers import Seats
from events.eventprocessor import SeatAssigner
from utils.logs import Logger

logging = Logger.get_logger()

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
    seats_assigninig_service = Seats()
    seat_assigner = SeatAssigner(seats_assigninig_service, requests_file, response_file)
    seat_assigner.process()
    print("Responses can be found at {}".format(os.path.abspath(response_file_name)))
