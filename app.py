from flask import *
from booking import *
import mechanicalsoup
import ast

app = Flask(__name__)

# setup browser and cookies
browser = mechanicalsoup.StatefulBrowser()
default_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/71.0.3578.98 Safari/537.36 "

default_date_format = "%Y-%m-%d"
default_base_url = "https://www.matchi.se"
default_schedule_url = "https://www.matchi.se/book/schedule?name=spangatbk&sport=1&indoor=true&facilityId=55&wl="
available_time_class = "courtLinks"


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/booking", methods=["POST"])
def booking():
    username = request.form["username"]
    password = request.form["password"]

    # login
    browser.open("https://www.matchi.se/login/auth")
    browser.select_form('#loginForm')
    browser["j_username"] = username
    browser["j_password"] = password
    browser.submit_selected()

    # set correct referer and UA in header to allow booking
    browser.session.headers["referer"] = browser.get_url()
    browser.session.headers["user-agent"] = default_user_agent

    booking_slots = get_booking_slots()

    return render_template("booking.html", booking_slots=booking_slots)


@app.route("/booked", methods=["POST"])
def book():
    slots = request.form.getlist("slot_checkbox")
    slots_parsed = []
    for slot in slots:
        slot = ast.literal_eval(slot)  # convert string representation of list to python list
        slot_parsed = TimeSlot(slot[0])
        slots_parsed.append(slot_parsed)
        add_entry(slot[0], slot[1], slot[2], slot[3])
    return render_template("booked.html", booked_slots=slots_parsed)


def get_booking_slots():
    days_to_get = []
    for day_offset in range(0, 5):
        day = datetime.today() + timedelta(days=day_offset)
        days_to_get.append(day.strftime(default_date_format))

    booking_slots = []
    for day in days_to_get:
        browser.open(default_schedule_url + "&date=" + day)
        timeslot_elements = browser.get_current_page().findAll("a", {"class": available_time_class})
        for timeslot_element in timeslot_elements:
            timeslot_url = default_base_url + timeslot_element["href"]
            timeslot = TimeSlot(timeslot_url)
            booking_slots.append(timeslot)

    return booking_slots


if __name__ == '__main__':
    app.run()
