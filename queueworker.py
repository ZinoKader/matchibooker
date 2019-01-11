import browsing
import slotqueue
import sys
import time
from tinydb import TinyDB, Query
from apscheduler.schedulers.background import BackgroundScheduler

bookingqueue_path = "resources/bookingqueue.json"
scheduler = BackgroundScheduler()
purging_interval_minutes = 0.1
booking_interval_minutes = 0.1


class QueueWorker:
    """
    QueueWorker should be run from terminal
    """
    def __init__(self, username, password):
        # matchi credentials needed to book queued slots
        self.browser = browsing.Browser()
        self.username = username
        self.password = password

    def purge_expired(self):
        slotqueue.delete_expired_slots()

    def try_booking(self):
        self.browser.matchi_login(self.username, self.password)
        db = TinyDB(bookingqueue_path)
        for slot in db:
            if self.browser.book_slot(slot["url"]):
                log_event("Booked slot with url " + slot["url"])
                db.remove(Query().url == slot["url"])
            else:
                log_event("Did not book slot with url " + slot["url"])
        db.close()


def log_event(text):
    log_file = open("resources/log.txt", "a", encoding="utf-8")
    log_file.write(text + "\n")
    log_file.close()


def stop_worker():
    scheduler.shutdown()
    sys.exit(0)


if __name__ == '__main__':
    username = "zinokad@gmail.com"
    print("Username : " + username)
    password = input("Please enter your password: ")
    queueWorker = QueueWorker(username, password)

    scheduler.add_job(queueWorker.purge_expired, "interval", minutes=purging_interval_minutes)
    print("Purging job started with " + str(purging_interval_minutes) + " minute intervals")
    scheduler.add_job(queueWorker.try_booking, "interval", minutes=booking_interval_minutes)
    print("Booking job started with " + str(booking_interval_minutes) + " minute intervals")
    scheduler.start()

    # run indefinitely
    while True:
        time.sleep(0.01)
