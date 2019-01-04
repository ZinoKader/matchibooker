from datetime import *

default_datetime_format = '%Y-%m-%d %H:%M:%S'
start_time_beginning = "start="
end_time_beginning = "end="
string_end = "&"


class TimeSlot:
    def __init__(self, booking_url):
        self.booking_url = booking_url
        self.start_time = booking_url[booking_url.find(start_time_beginning) +
                                      len(start_time_beginning): booking_url.rfind(string_end)]
        self.end_time = booking_url[booking_url.find(end_time_beginning) +
                                    len(end_time_beginning): booking_url.rfind(string_end)]

    def get_booking_url(self):
        return self.booking_url

    def get_start_time(self):
        return datetime.utcfromtimestamp(self.start_time).strftime(default_datetime_format)

    def get_end_time(self):
        return datetime.utcfromtimestamp(self.end_time).strftime(default_datetime_format)
