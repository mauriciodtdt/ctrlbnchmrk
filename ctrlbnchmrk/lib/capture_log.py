import logging
from logging.handlers import TimedRotatingFileHandler

DATA_PATH='../data/'

###########################################################
#Functions to log results and errors in csv and json format
###########################################################

#class LOGGER:
#   def __init__(self, logger_name, file_type)
#      self.logger_name = logger_name
#      self_file_type = file_type

FORMATTER_CSV = logging.Formatter('%(asctime)s;%(name)s;%(message)s')
FORMATTER_JSON = logging.Formatter('{"Test": %(name)s, "Message": {\
        "Time": %(asctime)s, "Measures": [%(message)s]}}')

def get_console_handler(file_type):
   console_handler = logging.StreamHandler()
   if (file_type == 'csv'):
      console_handler.setFormatter(FORMATTER_CSV)
#      print "formater csv"
   else:
      console_handler.setFormatter(FORMATTER_JSON)
#      print "formater json"
   return console_handler

def get_file_handler(logger_name, file_type):
   LOG_FILE = DATA_PATH + logger_name + '.' + file_type
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   if (file_type == 'csv'):
      file_handler.setFormatter(FORMATTER_CSV)
   else:
      file_handler.setFormatter(FORMATTER_JSON)
   return file_handler

def get_logger(logger_name,file_type):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler(file_type))
   logger.addHandler(get_file_handler(logger_name, file_type))
   logger.propagate = False # with this conf, it's rarely necessary to propagate the error
   return logger
