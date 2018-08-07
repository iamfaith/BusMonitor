# encoding=utf8
import logging
import conf


def setup_logger(name=None, level=logging.DEBUG):
    filehandler = logging.FileHandler(filename=conf.logfile, encoding="utf8")
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(filehandler)
    return logger
