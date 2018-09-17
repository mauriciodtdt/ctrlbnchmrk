#!/usr/bin/python

from cbenchConf import *
import subprocess
import logging
import re
import json
import sys
from logging.handlers import TimedRotatingFileHandler

################# 
#Functions to log results and errors
###############

FORMATTER = logging.Formatter("%(asctime)s;%(name)s;%(levelname)s;%(message)s")
LOG_FILE = "cbenchPerfTest.log"

def get_console_handler():
  console_handler = logging.StreamHandler()
  console_handler.setFormatter(FORMATTER)
  return console_handler
def get_file_handler():
  file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
  file_handler.setFormatter(FORMATTER)
  return file_handler
def get_logger(logger_name):
  logger = logging.getLogger(logger_name)
  logger.setLevel(logging.DEBUG) # better to have too much log than not enough
  logger.addHandler(get_console_handler())
  logger.addHandler(get_file_handler())
  logger.propagate = False # with this pattern, it's rarely necessary to propagate the error up to parent
  return logger

my_logger = get_logger("CBENCH")

#################
# Cbench run with parameters imported from cbenchConf file
################
i=0
while (i<LOOP):
  cmdcbench = "cbench -c %s -p %s -m %s -l %s -s %s -M %s -w %s -t" % (CONTROLLER_IP, CONTROLLER_PORT, MS_PER_TEST, TESTS_PER_SWITCH, NUM_SWITCHES, NUM_MACS, CBENCH_WARMUP) 
  cbench=subprocess.Popen(cmdcbench, stdout=subprocess.PIPE, shell=True)
  (output, err) = cbench.communicate()
  cbenchResults = output[output.index("RESULT"):]
  cbenchResults = cbenchResults.replace("\n", " ")
  switches = cbenchResults.split()[1]
  macs = NUM_MACS
  avg_num_flows = cbenchResults.split()[7].split('/')[2]
  json_results = {}
  results = "%s;%s;%s" % (switches,macs,avg_num_flows)
  my_logger.debug(results)

  i+=1
