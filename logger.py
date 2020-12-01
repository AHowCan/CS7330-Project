from pprint import pformat
from dearpygui.core import (log_debug,
                            log_info,
                            log_warning,
                            log_error)
from dearpygui.core import log as log_trace


def log(*args):
    print(args)
    log_info(args)


def plog(*args):
    formated = pformat(args)
    print(formated)
    log_info(formated)
