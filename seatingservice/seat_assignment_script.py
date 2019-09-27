import sys
import os
from app.controllers import Seats
from events.eventprocessor import SeatAssigner
from utils.logs import Logger
import utils

logging = Logger.get_logger()

if __name__ == "__main__":
    help_text = "seat_assignment_script.py: error: the following arguments are required: inputfile \n ex: {} inputfile.txt".format(
        "seat_assignment_script.py")

    # Check if the number of args is exactly 2
    if len(sys.argv) != 2:
        print(help_text)
        os._exit(1)

    if not os.path.isfile(sys.argv[1]):
        logging.error("Requires a file path\n{}".format(help_text))
        os._exit(1)

    inputfile = sys.argv[1]
    requests_file = open(inputfile, "r")
    response_file_name = "response.txt"                                 #"{}-out.txt".format(utils.path_leaf(inputfile))
    response_file = open(response_file_name, "w")                       # Opening a file to write
    seats_assigninig_service = Seats()                                  # Service which assigns seats (has post method)
    seat_assigner = SeatAssigner(seats_assigninig_service, requests_file, response_file)    # Initialising the seat assigner
    seat_assigner.process()                                                                 # Processing the events
    print("\nResponses can be found at {}\n".format(os.path.abspath(response_file_name)))
