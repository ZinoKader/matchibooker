import mechanicalsoup

# setup browser and cookies
default_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/71.0.3578.98 Safari/537.36 "

default_date_format = "%Y-%m-%d"
default_base_url = "https://www.matchi.se"
default_schedule_url = "https://www.matchi.se/book/schedule?name=spangatbk&sport=1&indoor=true&facilityId=55&wl="
default_payment_url = "https://www.matchi.se/bookingPayment/pay"
available_time_class = "courtLinks"


class Browser:

    def __init__(self):
        self.browser = mechanicalsoup.StatefulBrowser()

    def matchi_login(self, username, password):
        # login
        self.browser.open("https://www.matchi.se/login/auth")
        if "id=\"loginForm\"" not in self.browser.get_current_page().prettify():  # already logged in, no need to login
            return
        self.browser.select_form('#loginForm')
        self.browser["j_username"] = username
        self.browser["j_password"] = password
        self.browser.submit_selected()

        # set correct referer and UA in header to allow booking
        self.browser.session.headers["referer"] = self.browser.get_url()
        self.browser.session.headers["user-agent"] = default_user_agent

    def get_available_slot_urls(self, day):
        self.browser.open(default_schedule_url + "&date=" + day)
        timeslot_elements = self.browser.get_current_page().findAll("a", {"class": available_time_class})
        timeslot_urls = []
        for timeslot_element in timeslot_elements:
            timeslot_url = default_base_url + timeslot_element["href"]
            timeslot_urls.append(timeslot_url)
        return timeslot_urls

    def book_slot(self, slot):
        booking_status = False

        self.browser.open(slot)
        booking_page = self.browser.get_current_page()

        if not booking_page.find("form", id="confirmForm"):
            return False
        booking_page = self.browser.get_current_page()

        # get booking payload values
        try:
            player_email = booking_page.find("input", {"name": "playerEmail"}).get("value")
            coupon_id = booking_page.find("option").get("value")
            order_id = booking_page.find("input", {"name": "orderId"}).get("value")
            facility_id = booking_page.find("input", {"name": "facilityId"}).get("value")
            start = booking_page.find("input", {"name": "start"}).get("value")
            end = booking_page.find("input", {"name": "end"}).get("value")
            booking_payload = {"orderId": order_id, "facilityId": facility_id, "start": start, "end": end,
                               "method": "COUPON", "customerCouponId": coupon_id, "playerEmail": player_email}
            booking_response = self.browser.post(default_payment_url,
                                                 headers=self.browser.session.headers, data=booking_payload)
            booking_status = True if "Thank you for your booking!" in booking_response.text else False
        except AttributeError:  # happens when one of above can't be found on the page -> booking not possible
            print("There's already an active booking - did not book slot")

        return booking_status
