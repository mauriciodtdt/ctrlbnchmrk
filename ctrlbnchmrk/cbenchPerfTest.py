#!/usr/bin/python
#from cbenchConf import *
import subprocess
import logging
import re
import json
import sys
from logging.handlers import TimedRotatingFileHandler

sys.path.append('../etc/')
import config

CONTROLLER_IP=config.CBENCH_CONFIG['CONTROLLER_IP']
CONTROLLER_PORT=config.CBENCH_CONFIG['CONTROLLER_PORT']
MS_PER_TEST=config.CBENCH_CONFIG['MS_PER_TEST']
TESTS_PER_SWITCH=config.CBENCH_CONFIG['TESTS_PER_SWITCH']
NUM_SWITCHES=config.CBENCH_CONFIG['NUM_SWITCHES']
NUM_MACS=config.CBENCH_CONFIG['NUM_MACS']
CBENCH_WARMUP=config.CBENCH_CONFIG['CBENCH_WARMUP']
TEST_LOOP=config.CBENCH_CONFIG['TEST_LOOP']

DATA_PATH='../data/'

###########################################################
#Functions to log results and errors in csv and json format
###########################################################

FORMATTER_CSV = logging.Formatter("%(asctime)s;%(name)s;%(message)s")
LOG_FILE_CSV = "DATA_PATH/cbenchPerfTest.log"

FORMATTER_JSON = logging.Formatter("{\"Test\": %(name)s, \"Message\": {\"Time\": %(asctime)s, \"Measures\": [%(message)s]}}")
LOG_FILE_JSON = "DATA_PATCH/cbenchPerfTest.json"

def get_console_handler(f):
   console_handler = logging.StreamHandler()
   if (f == 'csv'):
      console_handler.setFormatter(FORMATTER_CSV)
#      print "formater csv"
   else:
      console_handler.setFormatter(FORMATTER_JSON)
#      print "formater json"
   return console_handler

def get_file_handler(f):
   if (f == 'csv'):
      file_handler = TimedRotatingFileHandler(LOG_FILE_CSV, when='midnight')
      file_handler.setFormatter(FORMATTER_CSV)
   else:
      file_handler = TimedRotatingFileHandler(LOG_FILE_JSON, when='midnight')
      file_handler.setFormatter(FORMATTER_JSON)
   return file_handler

def get_logger(logger_name,ff):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler(ff))
   logger.addHandler(get_file_handler(ff))
   logger.propagate = False # with this pattern, it's rarely necessary to propagate the error up to parent
   return logger
 
my_logger_csv = get_logger("CBENCHCSV",'csv')
#print my_logger_csv
my_logger_json = get_logger("CBENCHJSON",'json')
  
 ##########################################################
 # Cbench run with parameters imported from cbenchConf file
 ##########################################################
i=0
while (i<TEST_LOOP):
   cmdcbench = "cbench -c %s -p %s -m %s -l %s -s %s -M %s -w %s -t" % (CONTROLLER_IP, CONTROLLER_PORT, MS_PER_TEST, TESTS_PER_SWITCH, NUM_SWITCHES, NUM_MACS, CBENCH_WARMUP)
   cbench=subprocess.Popen(cmdcbench, stdout=subprocess.PIPE, shell=True)
   (output, err) = cbench.communicate()
   cbenchResults = output[output.index("RESULT"):]
   cbenchResults = cbenchResults.replace("\n", " ")
   switches = cbenchResults.split()[1]
   macs = NUM_MACS
   avg_num_flows = cbenchResults.split()[7].split('/')[2]
   results_csv = "%s;%s;%s" % (switches,macs,avg_num_flows)
   results_json = "{switches: %s, macs: %s, avg_num_flows: %s}" % (switches,macs,avg_num_flows)
   my_logger_csv.debug(results_csv)
   my_logger_json.debug(results_json)
   i+=1
