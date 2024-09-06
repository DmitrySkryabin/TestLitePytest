import logging


class Logger:

    def __init__(self, name):
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.INFO)
        self.log.handlers = []

        self.sh = logging.StreamHandler()
        self.sh.setFormatter(logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s"))
        self.log.addHandler(self.sh)
        

    def get_logger(self):
        return self.log
