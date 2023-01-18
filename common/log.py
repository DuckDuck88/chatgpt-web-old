import logging
import sys


def _get_logger():
    log = logging.getLogger('log')
    log.setLevel(logging.INFO)

    # file_handler = logging.FileHandler('/var/log/chatgpt.log')
    console_handle = logging.StreamHandler(sys.stdout)

    # file_handler.setLevel(logging.DEBUG)
    console_handle.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    console_handle.setFormatter(formatter)
    # file_handler.setFormatter(formatter)

    log.addHandler(console_handle)
    # log.addHandler(file_handler)

    return log


# 日志句柄
logger = _get_logger()
