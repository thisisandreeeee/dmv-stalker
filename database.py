import sqlite3
from datetime import datetime
from logger import Logger
import time

class DB:
    def __init__(self):
        self.logger = Logger()
        self.db = sqlite3.connect('dmv_db')
        self.cur = self.db.cursor()
        self.cur.execute('''
            CREATE table IF NOT EXISTS appointment(ts TEXT, location TEXT, appt_time TEXT);
        ''')
        self.db.commit()

    def insert(self, loc, appt_time):
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        if not self._is_processed(appt_time):
            appt_time = self._process_dt(appt_time)
        self.logger.log("Data is being inserted into table: %s (%s)" % (loc, appt_time))
        self.cur.execute('''
            INSERT INTO appointment(ts, location, appt_time) VALUES(?,?,?)''', (ts, loc, appt_time))
        self.db.commit()

    def appt_exists(self, loc, appt_time):
        appt_time = self._process_dt(appt_time)
        self.logger.log("Checking whether data exists in table: %s (%s)" %(loc, appt_time))
        self.cur.execute('''
            SELECT * FROM appointment WHERE location = ? AND appt_time = ?''', (loc, appt_time))
        rows = self.cur.fetchall()
        if not rows:
            self.logger.log("Data does not exist in table.")
            self.insert(loc, appt_time)
            return False
        else:
            self.logger.log("Checking if appointment has been recently shown.")
            all_tdelta = []
            for row in rows:
                ts = row[0]
                date_object = datetime.strptime(ts, "%Y%m%d%H%M%S")
                diff_seconds = (datetime.now() - date_object).seconds
                all_tdelta.append(diff_seconds / 60)
            if min(all_tdelta) <= 30:
                self.logger.log("Latest appointment was recently shown")
                return False
        return True

    def select_all(self):
        self.cur.execute('''
            SELECT * FROM appointment
        ''')
        rows = self.cur.fetchall()
        if rows:
            for row in rows:
                ts, location, dt = row
                date_object = datetime.strptime(dt, "%Y%m%d%H%M%S")
                dt_formatted = date_object.strftime('%A, %B %d, %Y at %I:%M %p')
                print("{}: {}".format(location, dt_formatted))

    def get_appointments_for(self, loc):
        self.cur.execute('''
            SELECT * FROM appointment WHERE location = ?
        ''', (loc,))
        rows = self.cur.fetchall()
        res = []
        if rows:
            for row in rows:
                location, dt = row
                date_object = datetime.strptime(dt, "%Y%m%d%H%M%S")
                dt_formatted = date_object.strftime('%A, %B %d, %Y at %I:%M %p')
                res.append(dt_formatted)
        return res

    def _process_dt(self, dt):
        date_object = datetime.strptime(dt, '%A, %B %d, %Y at %I:%M %p')
        dt = date_object.strftime("%Y%m%d%H%M%S")
        return dt

    def _is_processed(self, dt):
        return False if ',' in dt else True

    def close(self):
        self.db.close()
