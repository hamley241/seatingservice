from utils.config import Config
from copy import deepcopy
from models.seat import Seat
import re
import statistics

class Show(object):
    def __init__(self, name="default", movie_name=None, timings=None):
        self._name = name
        self._seats = self._init_seats_matrix()

    def get_name(self):
        return self._name

    def get_seats(self):
        return self._seats

    def _init_seats_matrix(self):
        seats_config = Config.get_data_map().get("theatre").get(self.get_name()).get("seats_matrix")
        seats_matrix = []
        print(seats_config)
        for cnt in range(0, len(seats_config)):
            seats_matrix.append(self._init_row_seats(cnt, seats_config))
        return seats_matrix

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
            return None

        seats_ = self.get_seats()
        seats_names = []
        for row in seats_:
            seats_names.append(str(self._get_row_seat_names(row)))
        return "\tSCREEN this way\n{}".format("\n".join(seats_names))

    def _get_row_seat_names(self, seats_row):
        return [str(item) for item in seats_row]

    def get_empty_seats(self):
        # Get list of things that are vacant row wise
        empty_seats = []
        for row in self.get_seats():
            empty_seats.append([str(int(seat.is_empty())) for seat in row])
        return empty_seats

    def find_consecutive_empty_seats(self, num_of_seats):
        empty_seats = self.get_empty_seats()
        consecutive_string = "".join(["1"]*num_of_seats)
        consecutive_re = re.compile(consecutive_string)
        for cnt, row in enumerate(empty_seats):
            row_string = "".join(row)
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
        return self.find_consecutive_empty_seats(num_of_seats)

    def book(self, seats_list=None,num_seats=0):
        if seats_list:
            return self._book_seats_list(seats_list)
        elif num_seats:
            seats_list = self.find_best_seats(num_seats)
            return self._book_seats_list(seats_list)
        else:
            #Raise an exception here
            return


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


if __name__ == "__main__":
    s = Show()
    print(s)
    for i in range(1,25):
        bs = s.book(num_seats=4)
        print("\t".join([str(item) for item in  bs]))
        print(s.get_empty_seats())
    # bs = s.book(num_seats=4)
    # print("\t".join([str(item) for item in  bs]))
