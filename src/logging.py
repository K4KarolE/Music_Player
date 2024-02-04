
import logging
from time import perf_counter

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename="log_file.log",
                    format='%(asctime)s %(message)s',
                    filemode='w') # w/a


def logger_runtime(func):

    def func_wrapper(*args, **kwargs):
        logger.info(f'START: {func.__name__}')
        timer_start = perf_counter()
        func_actioned = func(*args, **kwargs)
        timer_stop = perf_counter()
        logger.info(f'{func.__name__} - runtime: {str(timer_stop-timer_start)[:4]}')

        return func_actioned

    return func_wrapper



def logger_basic(msg):
    logger.info(msg)
        