
import logging
import logging.handlers
import os


class Logger:
    BASIC_LOG_FORMAT = "%(asctime)s:[%(levelname)s]:[%(name)s]: %(message)s"
    TIME_FORMAT = "%d/%b/%Y:%H:%M:%S"
    __loggers = dict()
    __logger = None

    @classmethod
    def get_logger(cls,name = None):
        if not cls.__logger:
            log_file = '/tmp/seatsservice.log'
            Logger.__logger = logging.getLogger(name)
            Logger.__logger.setLevel(logging.DEBUG)
            handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=500000000,backupCount=1) #500 mb file 500 * 1000000 bytes
            formatter = logging.Formatter(Logger.BASIC_LOG_FORMAT, Logger.TIME_FORMAT)
            handler.setFormatter(formatter)
            Logger.__logger.addHandler(handler)
            Logger.__loggers[name] = Logger.__logger
            return Logger.__logger
        return cls.__logger


