from scraper import Scraper
from settings import LOCATIONS
from bot import Bot
import time
from datetime import datetime

def run_once(bot):
    for location, office_id in LOCATIONS.items():
        scraper = Scraper()
        appt = scraper.i_want_an_appointment_at(office_id)
        if appt:
            msg = "{}\n{}".format(location, appt)
            bot.post_message(msg)

def is_daytime():
    curr_hour = datetime.now().hour
    return True if not 0 <= curr_hour <= 8 else False

def sleep_till_morning():
    sleep_in_hours = 8 - datetime.now().hour
    time.sleep(sleep_in_hours * 3600)    

if __name__ == "__main__":
    bot = Bot()
    while True:
        if is_daytime():
            run_once(bot)
            time.sleep(900)
        else:
            sleep_till_morning()
