"""
__Date__ : 2017/7/8
__Author__ : linyu
"""

import logging
import sys
from logging import Logger
from logging.handlers import TimedRotatingFileHandler

from util.path_util import pjoin, LOG_DIR

__date_formatter = '%Y-%m-%d %H:%M:%S'
__log_formatter = '[%(asctime)s](%(levelname)7s) %(filename)s[%(lineno)3d] - %(funcName)s : %(message)s'
__simple_formatter = '%(asctime)s - %(filename)s[%(lineno)3d] - %(levelname)s - %(message)s'
__result_formatter = '%(asctime)s\t%(message)s'

if sys.platform.startswith('linux'):
    __all_log_file = pjoin(LOG_DIR, 'all.log')
    __error_log_file = pjoin(LOG_DIR, 'error.log')
    __TESTING__ = False
else:
    __all_log_file = pjoin(LOG_DIR, 'test_all.log')
    __error_log_file = pjoin(LOG_DIR, 'test_error.log')
    # __TESTING__ = False
    __TESTING__ = True
__judge_log = pjoin(LOG_DIR, 'judge_result.log')
__segmentation_log = pjoin(LOG_DIR, 'segmentation.log')
__log_map = {
    'judge_result': __judge_log,
    'segmentation': __segmentation_log
}


def get_logger(logger_name='api', api_log=False, show_console=False):
    """Get logger by name
    :param logger_name: logger name
    :return initialized logger with given name
    """
    if logger_name not in Logger.manager.loggerDict:
        parsed = False
        for _name, _log_file in __log_map.items():
            if logger_name.startswith(_name):
                _logger = logging.getLogger(logger_name)
                _logger.setLevel(logging.DEBUG)
                result_handler = TimedRotatingFileHandler(_log_file, when='midnight', backupCount=20)
                result_formatter = logging.Formatter(__result_formatter, __date_formatter)
                result_handler.setFormatter(result_formatter)
                result_handler.setLevel(logging.INFO)
                _logger.addHandler(result_handler)
                parsed = True
                break
        if not parsed:
            _logger = logging.getLogger(logger_name)
            _logger.setLevel(logging.DEBUG)
            # handler all
            all_handler = TimedRotatingFileHandler(__all_log_file, when='midnight', backupCount=20)
            all_formatter = logging.Formatter(__log_formatter, __date_formatter)
            all_handler.setFormatter(all_formatter)
            all_handler.setLevel(logging.INFO)
            _logger.addHandler(all_handler)
            # handler error
            error_handler = TimedRotatingFileHandler(__error_log_file, when='midnight', backupCount=20)
            error_formatter = logging.Formatter(__log_formatter, __date_formatter)
            error_handler.setFormatter(error_formatter)
            error_handler.setLevel(logging.ERROR)
            _logger.addHandler(error_handler)

        if __TESTING__ or show_console:
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(__log_formatter)
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(logging.DEBUG)
            _logger.addHandler(console_handler)

    _logger = logging.getLogger(logger_name)
    return _logger


if __name__ == '__main__':
    logger = get_logger('data_service')
    logger.error('test - error')
    logger.info('test - info')
    logger.warn('test - warn')
