from datetime import *
import re

default_datetime_format = '%Y-%m-%d %H:%M:%S'
any_regex = "(.*)"
start_time_beginning = "start="
end_time_beginning = "end="
string_end = "&"


class TimeSlot:
    def __init__(self, booking_url):
        self.booking_url = booking_url
        self.start_time = float(re.search(start_time_beginning + any_regex + string_end, booking_url).group(1)[0])
        self.end_time = float(re.search(end_time_beginning + any_regex + string_end, booking_url).group(1)[0])

    def get_booking_url(self):
        return self.booking_url

    def get_start_time(self):
        return datetime.utcfromtimestamp(self.start_time).strftime(default_datetime_format)

    def get_end_time(self):
        return datetime.utcfromtimestamp(self.end_time).strftime(default_datetime_format)
