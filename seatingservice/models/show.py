from utils.config import Config
from copy import deepcopy
from models.seat import Seat
import re
import statistics
import numpy as np

class Show(object):
    def __init__(self, name="default", movie_name=None, timings=None):
        self._name = name
        self.row_names_index = None
        self._seats = None
        self._init_seats()

    def get_name(self):
        return self._name

    def get_seats(self):
        return self._seats

    def _init_seats(self):
        seats_config = Config.get_data_map().get("theatre").get(self.get_name()).get("seats_matrix")
        seats_matrix = []
        row_index_mapping = {}
        print(seats_config)
        for cnt in reversed(range(0, len(seats_config))):
            seats_matrix.append(self._init_row_seats(cnt, seats_config))
            row_index_mapping[seats_config[cnt].get("name")] = cnt
        self.row_names_index = row_index_mapping
        self._seats =  seats_matrix

    def _init_row_seats(self, cnt, seats_config):
        row_name = seats_config[cnt]["name"]
        number_of_seats = seats_config[cnt]["count"]
        seat_type = seats_config[cnt]["seat_type"]
        row_matrix = []
        for cnt in range(1, number_of_seats + 1):
            new_seat = Seat(row_name, cnt)
            row_matrix.append(new_seat)
        return row_matrix

    def __str__(self):
        if not self.get_seats():
            return ""

        seats_ = self.get_seats()
        seats_names = []
        for row in seats_:
            seats_names.append(str(self._get_row_seat_names(row)))
        return "{}\n\tSCREEN this way\n".format("\n".join(seats_names))

    def _get_row_seat_names(self, seats_row):
        return [str(item) for item in seats_row]

    def get_empty_seats(self):
        # Get list of things that are vacant row wise
        empty_seats = []
        for row in self.get_seats():
            empty_seats.append([int(seat.is_empty()) for seat in row])
        return empty_seats

    def get_empty_seats_count(self):
        return np.array(self.get_empty_seats()).sum()

    def find_consecutive_empty_seats(self, num_of_seats, empty_seats):
        consecutive_string = "".join(["1"]*num_of_seats)
        consecutive_re = re.compile(consecutive_string)
        for cnt, row in enumerate(empty_seats):
            row_string = "".join([str(item) for item in row])
            results = consecutive_re.finditer(row_string)
            results = list(results)
            if results:
                best = len(empty_seats[cnt])//2
                small_diff = statistics.mean([0,len(empty_seats[cnt])])
                res_match = None
                for res in results:
                    res_mean = statistics.mean(res.span())
                    new_diff = abs(res_mean- best)
                    if  new_diff < small_diff:
                        res_match = res
                        small_diff = new_diff
                print("Found consec")

                return self.get_seats()[cnt][res_match.span()[0]:res_match.span()[1]]
        return

    def find_best_seats(self, num_of_seats):
        # Use Regex to find consecutive empty seats
        empty_seats = self.get_empty_seats()
        selected_seats =  self.find_consecutive_empty_seats(num_of_seats, empty_seats)
        if not selected_seats:
            selected_seats = self.find_nonconsecutive_empty_seats(num_of_seats, empty_seats)
        return selected_seats

    def book(self, seats_names=None,num_seats=0, txn_id=None):
        seats_list = []
        if seats_names:
            #Check if the seats are empty
            seats_list = self._get_seats_from_names(seats_names)
            for seat in seats_list:
                if seat.is_booked():
                    print("Request for already booked seat")
                    #Raise an exception
                    return []
        elif num_seats:
            seats_list = self.find_best_seats(num_seats)
        else:
            #Raise an exception here
            return

        if seats_list:
            print("CAN assign")
            return self._book_seats_list(seats_list)
        else:
            print("Cant assign")
            return []

    
    def __book(self, seats_list):
        pass

    def _book_seats_list(self, seats_list):
        booked_list = []
        try:
            for item in seats_list:
                item.book()
                booked_list.append(item)
        except Exception as e:
            # log exception
            print(e)
            return False
        return booked_list

    def find_nonconsecutive_empty_seats(self, num_of_seats, empty_seats):
        empty_seats_arr =  np.array(empty_seats)
        rows_sum = empty_seats_arr.sum(axis=1)
        if np.sum(rows_sum) < num_of_seats:
            print("Cannot assign seats ")
            return []
        elif np.max(rows_sum) >= num_of_seats:
            row_indx = np.argmax(rows_sum>=num_seats)
            col_indices = (np.where(empty_seats_arr[row_indx] == 1)[0]).tolist()[:num_of_seats]
            print("DEBUG Assigning in a single row {}".format((str(num_of_seats))))
            return [s.get_seats()[row_indx][col_indx] for col_indx in col_indices]
        else:
            print("DEBUG Cannot assign in a single row {}".format((str(num_of_seats))))
            row_indexes, col_indices = np.where(empty_seats_arr == 1)
            return [s.get_seats()[row_indexes[cnt]][col_indices[cnt]] for cnt, item in enumerate(col_indices)][:num_of_seats]

    def _get_seats_from_names(self, seats_names):
        pass



if __name__ == "__main__":
    import random
    s = Show()
    print(s)
    for i in range(1,35):
        # num_seats = 4 if i <= 20 else random.randint(1,6)
        num_seats = random.randint(1,6)
        print("Seats requested {}".format(str(num_seats)))
        bs = s.book(num_seats=num_seats)
        print("\t".join([str(item) for item in  bs]))
        print("Empty seats count {}\n##########\n".format(s.get_empty_seats_count()))
    # bs = s.book(num_seats=4)
    # print("\t".join([str(item) for item in  bs]))
