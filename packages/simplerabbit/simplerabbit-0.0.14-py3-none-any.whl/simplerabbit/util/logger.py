import logging
from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self, log_path, logfile_prefix):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler = TimedRotatingFileHandler(log_path + '/' + logfile_prefix, when='midnight', interval=1)
        handler.suffix = '_%Y-%m-%d.log'
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def info(self, msg):
        self.logger.info(msg)
