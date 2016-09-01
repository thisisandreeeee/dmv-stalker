import sqlite3
from datetime import datetime
from logger import Logger

class DB:
    def __init__(self):
        self.logger = Logger()
        self.db = sqlite3.connect('dmv_db')
        self.cur = self.db.cursor()
        self.cur.execute('''
            CREATE table IF NOT EXISTS appointment(location TEXT, appt_time TEXT);
        ''')
        self.db.commit()

    def insert(self, loc, appt_time):
        if not self._is_processed(appt_time):
            appt_time = self._process_dt(appt_time)
        self.logger.log("Data is being inserted into table: %s (%s)" % (loc, appt_time))
        self.cur.execute('''
            INSERT INTO appointment(location, appt_time) VALUES(?,?)''', (loc, appt_time))
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
        return True

    def select_all(self):
        self.cur.execute('''
            SELECT * FROM appointment
        ''')
        rows = self.cur.fetchall()
        if rows:
            for row in rows:
                location, dt = row
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
