import statistics
import sys

import numpy as np
import re
from utils import numpy_fillna

from models.availableseats import AvailableSeats
from models.seatsrow import SeatsRow
from models.unassignedseats import NASeats
from models.screenlayout import ScreenLayout
from models.seat import VanillaSeat
import logging

class Screen(object):

    def __init__(self, layout_config, name="default"):
        self._name = name
        self._layout = ScreenLayout()
        self._unavailable_seats = NASeats()
        seats_conf = layout_config.get(self._name).get("seats_matrix")
        self._init_layout(seats_conf)
        self._init_seats_unavailable(seats_conf)
        self._total_seats_count = self.get_layout().get_total_size()

    def _init_layout(self, layout_config):
        for cnt, row_config in enumerate(reversed(layout_config)):
            row_name = row_config.get("name")
            row_seats = self._create_row_seats(row_config)
            self._layout.add_row(row_name, row_seats)
        return

    def _create_row_seats(self, row_config):
        seats_row = SeatsRow()
        row_name = row_config["name"]
        number_of_seats = row_config["count"]
        for col in range(1, number_of_seats + 1):
            new_seat = VanillaSeat(row_name, col)
            seats_row.add_seat(col, new_seat)
        return seats_row

    def _init_seats_unavailable(self, layout_config):

        for row_config in reversed(layout_config):
            row_name = row_config.get("name")
            empty_row = self._create_na_row(row_config)
            self.get_unavailable_seats().add_row(row_name, empty_row)
        return

    def get_unavailable_seats(self):
        return self._unavailable_seats

    def get_available_seats(self):
        pass  # return self.get_total_seats_count() - self.get_unavailable_seats().get_total_size()

    def get_total_seats_count(self):
        return self._total_seats_count

    def get_available_seats_count(self):
        print("Total seats {} Available seats {}".format(str(self.get_total_seats_count()),
                                                         str(self.get_unavailable_seats().get_total_size())))
        return self.get_total_seats_count() - self.get_unavailable_seats().get_total_size()

    def get_layout(self):
        return self._layout

    def _create_na_row(self, row_config):
        return set()

    def find_best_seats(self, num_of_seats):
        empty_seats = self.get_empty_seats()
        return empty_seats

    def get_empty_seats(self):
        """

        Returns:

        """
        # This is like a DB query, So filtering based on criteria has to be done

        empty_seats = AvailableSeats()
        for row, row_seats in self.get_layout().items():
            row_of_empty_seats = row_seats.keys() - self.get_unavailable_seats().get_row(row)
            empty_seats.add_row(row, row_of_empty_seats)
        return empty_seats

    def get_string_hash(self, numpy_arr):
        """
        Computes hash string for a 1D numpy array
        Args:
            numpy_arr: 1D numpy array

        Returns: String

        """
        return "".join([str(int(item)) for item in numpy_arr])

    def _get_consecutive_seats(self, empty_seats, num_of_seats):
        """
        Searches for consecutive seats among empty/vacant seats
        Args:
            empty_seats: AvailableSeats object that contains -> Row hashed Entries
            num_of_seats: number of seats to find

        Returns:  [] - An empty or  list containing Seat PKs/ names if found

        """

        consecutive_string = "".join(["1"] * num_of_seats)
        consecutive_re = re.compile(consecutive_string)
        for row, rowdata in empty_seats.items():
            boolarray = self.get_numpy_arr_wth_row_empty_indicators(row, rowdata)
            if boolarray.sum() >= num_of_seats:
                row_hash = self.get_string_hash(boolarray)
                results = list(consecutive_re.finditer(row_hash))
                if results:
                    return self._find_centered_consecutive(results, row)
        return []

    def _find_centered_consecutive(self, results, row):
        best = len(self.get_layout().get_row(row)) // 2
        small_diff = sys.maxsize
        res_match = None
        for res in results:
            res_mean = statistics.mean(res.span())
            new_diff = abs(res_mean - best)
            if new_diff < small_diff:
                res_match = res
                small_diff = new_diff
        print("Found consec")
        print(res_match.span())
        return [VanillaSeat.get_seat_name(row, col + 1) for col in
                range(res_match.span()[0], res_match.span()[1])]

    def find_nonconsecutive_empty_seats1(self, empty_seats, num_of_seats):
        empty_seats_arr = self.get_empty_seats_array(empty_seats)
        rows_sum = empty_seats_arr.sum(axis=1)
        if np.sum(rows_sum) < num_of_seats:
            print("Cannot assign seats ")
            return []
        elif np.max(rows_sum) >= num_of_seats:
            row_indx = np.argmax(rows_sum >= num_of_seats)
            col_indices = (np.where(empty_seats_arr[row_indx] == 1)[0]).tolist()[:num_of_seats]
            print("DEBUG Assigning in a single row {}".format((str(num_of_seats))))
            return [VanillaSeat.get_seat_name(list(empty_seats)[row_indx], col_indx + 1) for col_indx in col_indices]
        else:
            print("DEBUG Cannot assign in a single row {}".format((str(num_of_seats))))
            row_indexes, col_indices = np.where(empty_seats_arr == 1)
            return [VanillaSeat.get_seat_name(list(empty_seats)[row_indexes[cnt]], col_indices[cnt]) for cnt, item
                    in enumerate(col_indices)][
                   :num_of_seats]

    def find_nonconsecutive_empty_seats(self, empty_seats, num_of_seats):
        empty_seats_arr = np.array(
            [np.array(self.get_numpy_arr_wth_row_empty_indicators(row, item)) for row, item in empty_seats.items()])
        print(empty_seats_arr)
        empty_seats_arr = numpy_fillna(empty_seats_arr)
        print(empty_seats_arr)
        rows_sum = empty_seats_arr.sum(axis=1)
        if np.sum(rows_sum) < num_of_seats:
            print("Cannot assign seats ")
            return []
        if np.max(rows_sum) >= num_of_seats:
            return self.get_seats_from_same_row(empty_seats, empty_seats_arr, num_of_seats, rows_sum)

        # DEFAULT CASE GREEDY ASSIGNMENT
        logging.info("DEBUG Cannot assign in a single row {}".format((str(num_of_seats))))
        return self._get_seats_from_different_rows(empty_seats, num_of_seats)

    def get_seats_from_same_row(self, empty_seats, empty_seats_arr, num_of_seats, rows_sum):
        row_indx = np.argmax(rows_sum >= num_of_seats)
        col_indices = (np.where(empty_seats_arr[row_indx] == 1)[0]).tolist()[:num_of_seats]
        print("DEBUG Assigning in a single row {}".format((str(num_of_seats))))
        return [VanillaSeat.get_seat_name(list(empty_seats.keys())[row_indx], int(col) + 1) for col in
                col_indices]  # [s.get_seats()[row_indx][col_indx] for col_indx in col_indices]

    def _get_seats_from_different_rows(self, empty_seats, num_seats):
        found_seats = []
        for row, row_data in empty_seats.items():
            if len(found_seats) >= num_seats:
                break
            if len(row_data) != 0:
                found_seats = found_seats + [VanillaSeat.get_seat_name(row, col) for col in
                                             list(row_data)[:num_seats]]
                logging.debug(found_seats)
        return found_seats[:num_seats]

    def get_numpy_arr_wth_row_empty_indicators(self, row, empty_seats_row):
        """
        Creates a numpy array representation with 1 indicating empty seats in row
        for faster computations
        Args:
            empty_seats_row: Set containing the seats numbers which are empty

        Returns: 1D numpy array

        """
        zeros_arr = np.zeros(len(self.get_layout().get_row(row)) + 1)
        zeros_arr[list(empty_seats_row)] = 1
        zeros_arr = zeros_arr[1:]
        return zeros_arr

    def get_seats_to_assign(self, num_seats):
        empty_seats = self.get_empty_seats()
        consecutive_seats = self._get_consecutive_seats(empty_seats, num_seats)
        if not consecutive_seats:
            consecutive_seats = self.find_nonconsecutive_empty_seats(empty_seats, num_seats)
        if not consecutive_seats:
            print("Not able to assign this time")
        return consecutive_seats

    def book(self, num_seats, txn_id=None):
        seats_list = self.get_seats_to_assign(num_seats)
        return self._book(seats_list)

    def _book(self, seats_list):
        for seat in seats_list:
            if self.get_unavailable_seats().has(seat):
                print("isue")
            self.get_unavailable_seats().add(seat)
        return seats_list

    def get_empty_seats_array(self, empty_seats):
        arr_holder = []
        for row, row_data in empty_seats.items():
            empty_indicator = np.zeros(len(self.get_layout().get_row(row)) + 1)
            empty_indicator[list(row_data)] = 1
            arr_holder.append(empty_indicator[1:])
        return numpy_fillna(np.array(arr_holder))


from utils.config import Config
import time
if __name__ == "__main__":
    ti = time.time()
    conf = Config.get_data_map().get("theatre")
    scr = Screen(conf)
    es = scr.get_empty_seats()
    resp = scr.get_empty_seats_array(es)
    print(resp)
    print("""################3\n\n\n""")
    import random

    f = open("Debug.txt.1", "w")
    for i in range(1, 500):
        # num_seats = 4 if i <= 20 else random.randint(1,6)
        num_seats = random.randint(1, 30)
        print("Seats requested {}".format(str(num_seats)))
        f.write("\n\nSeats Request - " + str(num_seats))
        f.write("\nSeats total - " + str(scr.get_total_seats_count()))
        f.write("\nSeats total - " + str(scr.get_unavailable_seats().get_total_size()))
        bs = scr.book(num_seats=num_seats)
        f.write("\nSeats Available - " + str(scr.get_available_seats_count()))
        f.write("\nSeats Assigned - " + str(bs))
        print("\t".join([str(item) for item in bs]))
        print("Empty seats count {}\n##########\n".format(scr.get_available_seats_count()))
    print("Time taken :  {}".format(str((time.time()- ti))))