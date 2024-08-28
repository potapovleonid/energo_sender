import datetime
import logging
import os


class Logger:
    __date_now = datetime.datetime.now().strftime("%Y-%m-%d %H %M")
    __path_data = './log/'
    __log_path = __path_data + f'log {__date_now}.log'

    if not os.path.exists(__path_data):
        os.makedirs(__path_data)

    def __init__(self):
        super().__init__()

    def setup_logging(self):
        handler = logging.FileHandler(filename=self.__log_path,
                                      encoding='utf-8')
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().addHandler(handler)
