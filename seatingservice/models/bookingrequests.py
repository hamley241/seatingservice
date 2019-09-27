class BookingRequests(dict):
    """
    Acts like a table with PrimaryKey on Requests and FK on Seats
    """

    def get_seats(self, request_id):
        return self.get(request_id)

    def set(self, request_id, tickets_list):
        if not isinstance(tickets_list, list):
            raise TypeError()
        super().__setitem__(request_id, tickets_list)
