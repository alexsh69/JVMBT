from logging import StreamHandler
import logging
import sys

logger = logging.getLogger("service")
logger.setLevel(level=logging.INFO)
logger_formatter = logging.Formatter(
    "%(asctime)s -> %(filename)s -> %(funcName)s -> %(lineno)d :: [%(levelname)s] -> %(message)s")


def get_logger(logging_level=logging.INFO, debug=False):
    stream_handler = StreamHandler(stream=sys.stderr)
    stream_handler.setFormatter(fmt=logger_formatter)
    stream_handler.setLevel(level=logging_level)
    logger.addHandler(hdlr=stream_handler)
    logger.info(f"Logger initialized successfully! (debug={debug})")
    return logger
