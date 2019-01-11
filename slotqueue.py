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
        self.epoch_start_time = int(re.search(start_time_beginning + any_regex + start_time_string_end, booking_url).group(1)) / 1000
        self.epoch_end_time = int(re.search(end_time_beginning + any_regex + end_time_string_end, booking_url).group(1)) / 1000
        self.date = datetime.fromtimestamp(self.epoch_start_time).strftime(default_date_format)
        self.start_time = datetime.fromtimestamp(self.epoch_start_time).strftime(default_time_format)
        self.end_time = datetime.fromtimestamp(self.epoch_end_time).strftime(default_time_format)


def log_booking(text):
    log_file = open("resources/log.txt", "a", encoding="utf-8")
    log_file.write(datetime.now().strftime(default_date_format + " - " + default_time_format) + " - " + text + "\n")
    log_file.close()


def get_available_slots(browser):
    days_to_get = []
    for day_offset in range(0, 5):
        day = datetime.today() + timedelta(days=day_offset)
        days_to_get.append(day.strftime(default_date_format))

    booking_slots = []
    for day in days_to_get:
        for timeslot_url in browser.get_available_slot_urls(day):
            timeslot = TimeSlot(timeslot_url)
            booking_slots.append(timeslot)
    booking_slots.sort(key=lambda slot: slot.epoch_start_time)
    return booking_slots


def add_entry(url, date, start_time, end_time):
    db = TinyDB("resources/bookingqueue.json")
    db.insert({"url": url, "date": date, "start_time": start_time, "end_time": end_time})
    log_booking("Added slot with date " + date + " and time " + start_time + " - " + end_time)
    db.close()


def delete_expired_slots():
    db = TinyDB("resources/bookingqueue.json")
    for slot in db:
        slot_date = datetime.strptime(slot["date"], default_date_format).date()
        slot_time = datetime.strptime(slot["start_time"], default_time_format).time()
        if datetime.now().date() >= slot_date and datetime.now().time() >= slot_time:
            db.remove(Query().url == slot["url"])
            log_booking("Removed slot with date " + slot_date.strftime(default_date_format) +
                        " and time " + slot_time.strftime(default_time_format))
    db.close()
