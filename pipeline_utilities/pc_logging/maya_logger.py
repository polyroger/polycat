"""
This is just a maya subclass of the Pc_Logger, just so if there needs to be any
maya specific changes they wont effect other apps.

"""


from pc_logging.pc_logger import Pc_Logger

class Maya_Logger(Pc_Logger):

    LOGGER_NAME = "maya_logger"

    PROPAGATE = True

