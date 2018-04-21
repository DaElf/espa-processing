''' Provides the logging configuration tools '''

import sys
import logging


DATE_FMT = r'%Y-%m-%d %H:%M:%S'
LOG_LINE_FORMAT = (
    '%(asctime)s.%(msecs)03d %(process)d %(levelname)-8s '
    '%(filename)s:%(lineno)d:%(funcName)s -- %(message)s'
)


def configure_base_logger(stream='stdout', format=LOG_LINE_FORMAT,
                          datefmt=DATE_FMT, level='INFO'):
    """ Configures the base logger to an output stream

    Args:
        stream (str): The name of the output stream (stderr/stdout)
        format (str): The formatting to use withiin the log lines
        datefmt (str): The format for the date strings
        level (str): The base level of errors to log to the handler
    """
    logging.basicConfig(stream=getattr(sys, stream.lower()),
                        format=format,
                        datefmt=datefmt,
                        level=getattr(logging, level.upper()))
