from datetime import *
import re
from tinydb import TinyDB, Query

default_date_format = "%Y-%m-%d"
default_time_format = '%H:%M'
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


def log(text):
    log_file = open("resources/log.txt", "a", encoding="utf-8")
    log_file.write(datetime.now().strftime(default_date_format + " - " + default_time_format) + " - " + text + "\n")
    log_file.close()


def add_entry(url, date, start_time, end_time):
    db = TinyDB("resources/bookings.json")
    db.insert({"url": url, "date": date, "start_time": start_time, "end_time": end_time})
    log("Added slot with date " + date + " and time " + start_time + " - " + end_time)
    db.close()


def delete_expired_slots():
    db = TinyDB("resources/bookings.json")
    for slot in db:
        slot_date = datetime.strptime(slot["date"], default_date_format).date()
        slot_time = datetime.strptime(slot["start_time"], default_time_format).time()
        if datetime.now().date() >= slot_date and datetime.now().time() >= slot_time:
            db.remove(Query().url == slot["url"])
            log("Removed slot with date " + slot_date.strftime(default_date_format) +
                " and time " + slot_time.strftime(default_time_format))
    db.close()






