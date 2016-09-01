import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        LOG_DEST = 'logs/'
        if not os.path.exists(LOG_DEST):
            os.makedirs(LOG_DEST)
        self.LOG_DEST = LOG_DEST + '{}.log'

    def _update_config(self):
        curr_date = datetime.now().strftime("%Y%m%d")
        logging.basicConfig(
            filename = self.LOG_DEST.format(curr_date),
            filemode = 'a',
            format = '(%(asctime)s) %(name)s | %(message)s',
            datefmt = '%H:%M:%S',
            level = logging.INFO
        )

    def log(self, msg):
        self._update_config()
        logging.info(msg)
