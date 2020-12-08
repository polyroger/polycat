"""
This is the logging class for logging feedback at polycat
To create new rules for log formtting inherit this class and add your methods
"""

import logging
import sys


class Pc_Logger(object):
    """
    These are reminders of the log levels
        pc_log.critical("critical messege goes here") - 50
        pc_log.error("error messege goes here") -40 
        pc_log.warning("warning messege goes here") - 30
        pc_log.info("info messege goes here") - 20
        pc_log.debug("debug messege goes here") - 10
        pc_log.exception("this goes in the except block") - called in handler
        pc_log.log(25,"this is a custom log message") - custom level

    This design is nice because you dont have to create a class instance before you call the the methods. The get_logger_object method makes sure that the object
    gets created internally in the class method. Logging objects get stored in a dict that gets managed by the Logging class in the logging module. This allows you
    to create other class methoods that act on that class object without actually initializing it in the script.

    To use this class set a log level with Pc_Logger.set_log_level(level), if you want differnet logging levels try extending / subclassing the class 

    """
    LOGGER_NAME = "pc_log"
    DEFAULT = logging.DEBUG
    FORMATTING = "------------------\n[%(asctime)s] [%(levelname)s] [%(name)s]\n%(message)s"
    PROPAGATE = True

    _log_obj = None

    @classmethod
    def get_logger_object(cls):

        if not cls._log_obj:

            if cls.check_if_logger_exists():
                
                cls._log_obj = logging.getLogger(cls.LOGGER_NAME)

            else:

                cls._log_obj = logging.getLogger(cls.LOGGER_NAME)
                cls._log_obj.setLevel(cls.DEFAULT)
                cls._log_obj.propagate = cls.PROPAGATE

                log_format = logging.Formatter(cls.FORMATTING)
                stream_handler = logging.StreamHandler(sys.stderr)
                stream_handler.setFormatter(log_format)
                cls._log_obj.addHandler(stream_handler)

        return cls._log_obj

    @classmethod
    def check_if_logger_exists(cls):

        return  cls.LOGGER_NAME in logging.Logger.manager.loggerDict.keys()

    @classmethod
    def set_log_level(cls,level):

        level_logger = cls.get_logger_object()
        level_logger.setLevel(level)
    
    @classmethod
    def set_propagation(cls,propagate):
        """
        Stops child logging objects being inherited by parent loggin objects. Can cause duplication in dcc apps that use the python loggin module
        ARGS
        propagate (bool) - Whether to allow propogation or not
        """
        propagate_logger = cls.get_logger_object()
        propagate_logger.propagate = propagate


    @classmethod
    def write_log_to_file(cls,path,level=logging.DEBUG):
        """
        Writing to a file uses a different formatter and stream handler so as not to change the default logger.
        This will only write logs for events after it has been called. So dont put this at the bottom of your script.
        """
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(cls.FORMATTING)
        file_handler.setFormatter(file_formatter)

        file_logger = cls.get_logger_object()
        file_logger.addHandler(file_handler)


    @classmethod
    def debug(cls,message,*args,**kwargs):
        
        debug_logger = cls.get_logger_object()
        debug_logger.debug(message,*args,**kwargs)

    @classmethod
    def info(cls,message,*args,**kwargs):
        
        info_logger = cls.get_logger_object()
        info_logger.debug(message,*args,**kwargs)

    @classmethod
    def warning(cls,message,*args,**kwargs):
        
        warning_logger = cls.get_logger_object()
        warning_logger.debug(message,*args,**kwargs)

    @classmethod
    def error(cls,message,*args,**kwargs):
        
        error_logger = cls.get_logger_object()
        error_logger.debug(message,*args,**kwargs)

    @classmethod
    def critical(cls,message,*args,**kwargs):
        
        critical_logger = cls.get_logger_object()
        critical_logger.debug(message,*args,**kwargs)

    @classmethod
    def exception(cls,message,*args,**kwargs):
        """
        Only call this in an exception handler ( try except block )
        """
        
        exception_logger = cls.get_logger_object()
        exception_logger.exception(message,*args,**kwargs)

    @classmethod
    def log(cls,level,message,*args,**kwargs):
        
        log_logger = cls.get_logger_object()
        log_logger.log(level,message,*args,**kwargs)    
    


if __name__ == "__main__":
    Pc_Logger.set_log_level(1)
    Pc_Logger.write_log_to_file("logfile.log",1)
    Pc_Logger.set_propagation(False)

    Pc_Logger.debug("this is debug")
    Pc_Logger.log(5,"this is a custom log")

    try:
        a = []
        b = a[0]
    except:
        Pc_Logger.exception("Error in getting and index from A")





