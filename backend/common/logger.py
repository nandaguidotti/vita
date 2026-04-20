import os
import logging
import sys
from os.path import sep
from backend.common.path_finder import path_log
from logging.handlers import RotatingFileHandler

exclusive_logger_list = []
logger = None


class Logger:
    """
    log.debug('This is a debug message')
    log.info('This is an info message')
    log.warning('This is a warning message')
    log.error('This is an error message')
    log.critical('This is a critical message')
    log.exception(e)    # show the error message and the stacktrace
    """

    def __init__(self, module):
        if type(module) is not str:
            raise TypeError("Logger module must be a srt type, "
                            "but has found: %s" % str(type(module)))
        if module in exclusive_logger_list:
            raise ValueError("Logger module must be exclusive, "
                             "but other instance of '%s' is already running"
                             % str(module))
        else:
            exclusive_logger_list.append(module)

        self.module = module
        self.FORMATTER = logging.Formatter(fmt="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
                                           datefmt='%Y-%m-%d %H:%M:%S')
        try:
            if not os.path.isdir(self.path()):
                os.makedirs(self.path())
                if logger is not None:
                    logger.log.debug("Directory created successfully: '%s'" % self.path())
            else:
                if logger is not None:
                    logger.log.debug("Directory cheked successfully: '%s'" % self.path())
        except OSError as error:
            if logger is not None:
                logger.log.warning("Directory can not be created: '%s'" % self.path())
                logger.log.exception(error)

        self.LOG_FILE = self.path() + sep + module+'.log'
        self.log = self.__create_logger()
        self.log.debug("--- %s starts ---" % self.module)

    def path(self):
        return path_log(self.module)

    def __get_console_handler(self):
        """
        configure to sends logger messages to console
        :return: logging handler
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.FORMATTER)
        return console_handler

    def __get_file_handler(self):
        """
        configure to saves logger messages to file
        :return: logging handler
        """
        # Create the rotating file handler. Limit the size to 10000000Bytes ~ 10MB .
        file_handler = RotatingFileHandler(self.LOG_FILE, maxBytes=10000000, backupCount=1)
        file_handler.setFormatter(self.FORMATTER)
        return file_handler

    def __create_logger(self):
        """
        create and returns a logger
        :return: the logger configured
        """
        logger = logging.getLogger(self.module)
        logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
        logger.addHandler(self.__get_console_handler())
        logger.addHandler(self.__get_file_handler())
        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        return logger


logger = Logger("app")   # grava logs em /log/app/app.log

