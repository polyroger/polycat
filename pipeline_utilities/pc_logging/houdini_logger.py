"""
This is just a houdini subclass of the Pc_Logger, just so if there needs to be any
houdini specific changes they wont effect other apps.

"""


from pc_logging.pc_logger import Pc_Logger

class Houdini_Logger(Pc_Logger):

    LOGGER_NAME = "houdini_logger"

    PROPAGATE = True

