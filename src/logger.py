#
#
#
import logging

# msg_format = "%(asctime)s.%(msecs)03d %(levelname)s %(threadName)s %(filename)s:%(lineno)s %(message)s"
msg_format = "%(asctime)s.%(msecs)03d %(levelname)s %(message)s"
date_format = '%m%d.%H%M%S'

# log_level = logging.DEBUG
log_level = logging.INFO

log_file_path = '/tmp/modem-monitor.log'


def create_logger(log_file_path: str, log_level: int) -> logging.Logger:
    '''
    Get the logger object to use for logging.
    '''
    logging.basicConfig(
        level=log_level,
        # filename=log_file_path,
        format=msg_format, datefmt=date_format)
    log = logging.getLogger()

    return log


log = create_logger(log_file_path, log_level)


def get_logger() -> logging.Logger:
    return log
