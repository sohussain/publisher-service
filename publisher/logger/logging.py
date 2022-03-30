"""
@discription: set logging config
"""
import logging
import sys


def set_logging(level='DEBUG', stream=sys.stdout):
    root_logger = logging.getLogger("")
    root_logger.setLevel(level)
    FORMATTER = logging.Formatter(
        "%(asctime)s — %(threadName)s — %(levelname)s — %(message)s")
    ch = logging.StreamHandler(stream)
    ch.setFormatter(FORMATTER)
    root_logger.addHandler(ch)
