from scraper import Scraper
from settings import LOCATIONS
from bot import Bot
from database import DB
from logger import Logger
import time
from datetime import datetime

class App:
    def __init__(self):
        self.db = DB()
        self.logger = Logger()
        self.bot = Bot()

    def run(self):
        self.logger.log("App start")
        if self._is_daytime():
            self.logger.log("Is daytime, start run_once")
            self.run_once()
            self.logger.log("End run_once")
            time.sleep(900)
        else:
            self.logger.log("Is night, going to sleep")
            self._sleep_till_morning()
            self.logger.log("Waking up from sleep")

    def run_once(self):
        for location, office_id in LOCATIONS.items():
            scraper = Scraper()
            self.logger.log("Checking appointment for %s" % location)
            appt = scraper.i_want_an_appointment_at(office_id)
            if appt:
                self.logger.log("Appointment retrieved from web page")
                if not self.db.appt_exists(location, appt):
                    self.logger.log("New appointment found. Added to DB.")
                    msg = "*{}*\n{}".format(location, appt)
                    self.bot.post_message(msg)
                else:
                    self.logger.log("Appointment already exists in DB.")
            else:
                self.logger.log("Invalid appointment object returned")

    def _is_daytime(self):
        curr_hour = datetime.now().hour
        # return True if not 0 <= curr_hour <= 8 else False
        return True

    def _sleep_till_morning(self):
        sleep_in_hours = 8 - datetime.now().hour
        time.sleep(sleep_in_hours * 3600)

if __name__ == "__main__":
    app = App()
    while True:
        app.run()
