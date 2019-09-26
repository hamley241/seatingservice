import statistics
import sys
import numpy as np
import re
from utils import numpy_fillna
from utils.constants import SeatStatus
from models.availableseats import AvailableSeats
from models.seatsrow import SeatsRow
from models.unassignedseats import UnavailableSeats
from models.seatslayout import SeatsLayout
from models.seat import Seat
from utils.logs import Logger
import utils

logging = Logger.get_logger()


class Screen(object):
    """
    A screen in theatre, it HAS seats layout, HAS UnavailableSeats (currenlty supports booked type)
    Like an ORM object
    """

    def __init__(self, layout_config, name="default"):
        self._name = name
        self._layout = SeatsLayout()
        self._unavailable_seats = UnavailableSeats()
        seats_conf = layout_config.get(self._name).get("seats_matrix")
        self._init_layout(seats_conf)
        self._init_unavailable_seats(seats_conf)
        self._total_seats_count = self.get_layout().get_total_size()

    def _init_layout(self, layout_config):
        """
        initializes the layout of seats in form of SeatsLayout obj  which can be referred for geometry
        Args:
            layout_config: A list containing the dicts with details layout

        Returns: None

        """
        for cnt, row_config in enumerate(reversed(layout_config)):
            row_name = row_config.get("name")
            row_seats = self._create_row_seats(row_config)
            self._layout.add_row(row_name, row_seats)
        return

    def _create_row_seats(self, row_config):
        """
        Creates row of seats in form os SeatsRow from row config of seats
        Args:
            row_config: Dict,  row config of seats

        Returns: SeatsRow obj

        """
        seats_row = SeatsRow()
        row_name = row_config["name"]
        number_of_seats = row_config["count"]
        for col in range(1, number_of_seats + 1):
            new_seat = Seat(row_name, col)
            seats_row.add_seat(col, new_seat)
        return seats_row

    def _init_unavailable_seats(self, layout_config):
        """
        Initializes the UnavailableSeats obj which is like a datastore to store the unavailable objects
        Args:
            layout_config: config of seats layout

        Returns: None

        """

        for row_config in reversed(layout_config):
            row_name = row_config.get("name")
            available_row = self._create_unavailable_row(row_config)
            self.get_unavailable_seats().add_row(row_name, available_row)
        return

    def get_unavailable_seats(self):
        """
        Getter method for unavailable objects
        Returns: Return unavailabe seats attribute of self

        """
        return self._unavailable_seats

    def get_total_seats_count(self):
        """

        Returns: int, total number of seats in in seatsLayout => screen

        """
        return self._total_seats_count

    def get_available_seats_count(self):
        """

        Returns: int, returns total number of available seats

        """
        logging.debug("Total seats {} Unavailable seats {}".format(str(self.get_total_seats_count()),
                                                         str(self.get_unavailable_seats().get_total_size())))
        return self.get_total_seats_count() - self.get_unavailable_seats().get_total_size()

    def get_layout(self):
        return self._layout

    def _create_unavailable_row(self, row_config):
        """
        Creates row of unavailable seats in form of set from row config of seats
        Args:
            row_config: Dict,  row config of seats

        Returns: set

        """
        return set()

    def _get_available_seats(self):
        """
        Filters out seats remaining ( can add criteria to filter out based on types if needed)
        Returns: AvailableSeats obj containing seats that can be used for assigning

        """
        # This is like a DB query, So filtering based on criteria has to be done

        available_seats = AvailableSeats()
        for row, row_seats in self.get_layout().items():
            row_of_available_seats = row_seats.keys() - self.get_unavailable_seats().get_row(row)
            available_seats.add_row(row, row_of_available_seats)
        return available_seats

    def _get_string_hash(self, numpy_arr):
        """
        Computes hash string for a 1D numpy array
        Args:
            numpy_arr: 1D numpy array

        Returns: String

        """
        return "".join([str(int(item)) for item in numpy_arr])

    def _find_consecutive_seats(self, available_seats, num_of_seats):
        """
        Searches for consecutive seats among available/vacant seats
        Args:
            available_seats: AvailableSeats object that contains -> Row hashed Entries
            num_of_seats: number of seats to find

        Returns:  [] - An available or  list containing Seat PKs/ names if found

        """

        consecutive_string = r"(?="+"".join(["1"] * num_of_seats)+")"
        # consecutive_re = re.compile(consecutive_string)
        consecutive_re = re.compile(r"(?="+consecutive_string+")")
        available_seats_indicator_arr = self.get_available_seats_indicator_array(available_seats)
        for cnt, (row, rowdata) in enumerate(available_seats.items()):
            # available_seats_indicator_arr = self.get_numpy_arr_wth_row_available_indicators(row, rowdata)
            if available_seats_indicator_arr[cnt].sum() >= num_of_seats:
                row_hash = self._get_string_hash(available_seats_indicator_arr[cnt])
                results = list(consecutive_re.finditer(row_hash))
                if results:
                    return self._find_centered_consecutive(results, row, num_of_seats)
        return []

    def _find_centered_consecutive(self, consecutive_search_results, row, num_seats):
        """
        Finds the seats close to center of screen
        Args:
            consecutive_search_results: Results of regex findIter with span or should contain span with start and end of consec sequence
            row: Row Identifier (Like row PK  of seat)

        Returns: [] a list containing identifiers of consec seats

        """
        best_position = self._get_best_seat_position(row)
        smallest_mean_diff = sys.maxsize
        best_search_result = None
        for search_result in consecutive_search_results:
            res_mean = statistics.mean([search_result.span()[0], search_result.span()[0]+num_seats])
            distance_between_means = abs(res_mean - best_position)
            if distance_between_means < smallest_mean_diff:
                best_search_result = search_result
                smallest_mean_diff = distance_between_means
        logging.debug(
            "Found consecutive search results for {} seats in Row {}".format(str(best_search_result.span()), str(row)))
        return [Seat.get_seat_name(row, col + 1) for col in
                range(best_search_result.span()[0], best_search_result.span()[0]+num_seats)]

    def _get_best_seat_position(self, row):
        """
        Find the center most position of seat in given row based on seats layout config
        Args:
            row: Row identifier

        Returns: col, seat position in a given row

        """
        best_position = len(self.get_layout().get_row(row)) // 2
        return best_position

    def _find_nonconsecutive_available_seats(self, available_seats, num_of_seats):
        """
        Finds non-Consecutive available seats that can be assigned
        Args:
            available_seats: AvailableSeats obj containing seats that can be assigned
            num_of_seats: number of seats to find

        Returns: [] A list containing the P/identifiers of seats that can be assigned

        """
        available_seats_arr = self.get_available_seats_indicator_array(available_seats)
        row_wise_sum = available_seats_arr.sum(axis=1)
        if not self._can_find_available(row_wise_sum, num_of_seats):
            logging.debug("Cannot assign seats seats ")
            return []
        if self._can_find_available_in_same_row(row_wise_sum, num_of_seats):
            return self._find_seats_from_same_row(available_seats, available_seats_arr, num_of_seats, row_wise_sum)

        # DEFAULT CASE GREEDY ASSIGNMENT
        logging.debug("Cannot assign in a single row {} ".format((str(num_of_seats))))
        return self._find_seats_from_different_rows(available_seats, num_of_seats)

    def _can_find_available(self, rows_sum, num_of_seats):
        """
        Check if the screen has enough number of available seats to find
        Args:
            rows_sum: Row wise sum of each row of theatre
            num_of_seats: int, number of seats to find

        Returns: bool, indicating if the screen has enough seats

        """
        return sum(rows_sum) >= num_of_seats

    def _can_find_available_in_same_row(self, row_wise_sum, num_of_seats):
        """
        Checks if screen has enough available seats in single row to accomodate
        Args:
            row_wise_sum: list /numpy array containing row wise available seats sum
            num_of_seats: number of available seats to find

        Returns: bool, True if required number of seats are available in same row else False

        """
        return max(row_wise_sum) >= num_of_seats

    def _find_seats_from_same_row(self, available_seats, available_seats_arr, num_of_seats, rows_sum):
        """
        Finds seats in same row from available seats
        Args:
            available_seats: AvailableSeats obj
            available_seats_arr: Indicator array with 1s at available locations
            num_of_seats: Number of seats to find
            rows_sum: Array  containing row wise sum

        Returns:

        """
        row_indx = int(np.argmax(rows_sum >= num_of_seats))
        col_indices = (np.where(available_seats_arr[row_indx] == 1)[0]).tolist()[:num_of_seats]
        logging.debug("Assigning in a single row: num of seat - {} ".format((str(num_of_seats))))
        return [Seat.get_seat_name(list(available_seats.keys())[row_indx], int(col) + 1) for col in
                col_indices]

    def _find_seats_from_different_rows(self, available_seats, num_seats):
        """
        Finds seats from different rows
        Args:
            available_seats: AvailableSeats object
            num_seats: number of seats to find

        Returns: [], a list containing available seats that can be booked

        """
        found_seats = []
        for row, row_data in available_seats.items():
            if len(found_seats) >= num_seats:
                break
            if len(row_data) != 0:
                found_seats = found_seats + [Seat.get_seat_name(row, col) for col in
                                             list(row_data)[:num_seats]]
                logging.debug(found_seats)
        return found_seats[:num_seats]

    def get_numpy_arr_wth_row_available_indicators(self, row, available_seats_row):
        """
        Creates a numpy array representation with 1 indicating available seats in row
        for faster computations
        Args:
            available_seats_row: Set containing the seats numbers which are available

        Returns: 1D numpy array

        """
        zeros_arr = np.zeros(len(self.get_layout().get_row(row)) + 1)
        zeros_arr[list(available_seats_row)] = 1
        zeros_arr = zeros_arr[1:]
        return zeros_arr

    def _find_available_seats_to_assign(self, available_seats, num_seats):
        """
        Finds the required number of seats from availanble seats
        Args:
            available_seats: AvailableSeats obj containing available seats info
            num_seats: Number of seats to search for

        Returns: [], list of available seats

        """
        consecutive_seats = self._find_consecutive_seats(available_seats, num_seats)
        if consecutive_seats:
            return consecutive_seats
        non_consecutive_seats = self._find_nonconsecutive_available_seats(available_seats, num_seats)
        if non_consecutive_seats:
            return non_consecutive_seats
        logging.debug("No seats found for request of {} seats ".format(str(num_seats)))
        return consecutive_seats

    def book(self, num_seats, txn_id=None):
        """
        Reserves the number of seats if seats are available for reserving
        Args:
            num_seats: int number of seats to reserve
            txn_id: Txn Id associated with reservation

        Returns: [] A list of seats reserved

        """
        try:
            num_seats = utils.validate_positive_int(num_seats)
        except Exception as e:
            raise ValueError()
        available_seats = self._get_available_seats()
        seats_list = self._find_available_seats_to_assign(available_seats, num_seats)
        if seats_list:
            return self._book(seats_list)
        logging.error("No seats found for request {} of {} - Current available seats {} ".format(str(num_seats),
                                                                                                 str(txn_id),
                                                                                                 str(
                                                                                                     available_seats.get_total_size())))
        return seats_list

    def _book(self, seats_list, status=SeatStatus.BOOKED):
        """
        Marks a seat for given Screen at show timings as Unavaiable
        Data should be validated before calling this method (though safe checks are in place)
        Args:
            seats_list: List of seats with PKs/seat identifiers
            status: Returns list of seats marked

        Returns: []. list of seats booked

        """
        for seat in seats_list:
            if self.get_unavailable_seats().has(seat):
                raise Exception()
            self.get_unavailable_seats().add(seat)
        return seats_list

    def get_available_seats_indicator_array(self, available_seats):
        """
        Marks the available seats as 1 in a binary array in SeatsLayout structure with zeros padded for making it homogenous
        Args:
            available_seats: AvailableSeats obj

        Returns: numpy array - np.array

        """
        arr_holder = []
        for row, row_data in available_seats.items():
            available_indicator = np.zeros(len(self.get_layout().get_row(row)) + 1)
            available_indicator[list(row_data)] = 1
            arr_holder.append(available_indicator[1:])
        return numpy_fillna(np.array(arr_holder))


from utils.config import Config
import time

if __name__ == "__main__":
    ti = time.time()
    conf = Config.get_data_map().get("theatre")
    scr = Screen(conf)
    es = scr._get_available_seats()
    resp = scr.get_available_seats_indicator_array(es)
    print(resp)
    print("""################3\n\n\n""")
    import random

    # f = open("Debug.txt.1", "w")
    for i in range(1, 55):
        num_seats = random.randint(1, 10)
        print("Seats requested {}".format(str(num_seats)))
        bs = scr.book(num_seats=num_seats)
        # logging.info("\t".join([str(item) for item in bs]))
        logging.info("available seats count {}\n##########\n".format(scr.get_available_seats_count()))
        es = scr._get_available_seats()
        resp = scr.get_available_seats_indicator_array(es)
        # print(resp)
    logging.info("Time taken :  {}".format(str((time.time() - ti))))
