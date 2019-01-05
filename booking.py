from datetime import *
import re

default_date_format = "%Y-%m-%d"
default_time_format = '%H:%M:%S'
any_regex = "(.*)"
start_time_beginning = "start="
end_time_beginning = "end="
start_time_string_end = "&end"
end_time_string_end = "&sportIds"


class TimeSlot:
    def __init__(self, booking_url):
        self.booking_url = booking_url
        start_time_seconds = int(re.search(start_time_beginning + any_regex + start_time_string_end, booking_url).group(1)) / 1000
        end_time_seconds = int(re.search(end_time_beginning + any_regex + end_time_string_end, booking_url).group(1)) / 1000
        self.date = datetime.utcfromtimestamp(start_time_seconds).strftime(default_date_format)
        self.start_time = datetime.utcfromtimestamp(start_time_seconds).strftime(default_time_format)
        self.end_time = datetime.utcfromtimestamp(end_time_seconds).strftime(default_time_format)
