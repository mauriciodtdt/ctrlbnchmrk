#!/usr/bin/python
import subprocess
import logging
import time
import re
import json
import sys
import lib.capture_log as caplog
sys.path.append('/opt/ctrlbnchmrk/etc/')
import config

#Import CBENCH variables from configuration file /etc/config.py
CONTROLLER_IP=config.CONF['CONTROLLER_IP']
CONTROLLER_PORT=config.CONF['CONTROLLER_PORT']
MS_PER_TEST=config.CBENCH_CONFIG['MS_PER_TEST']
TESTS_PER_SWITCH=config.CBENCH_CONFIG['TESTS_PER_SWITCH']
NUM_SWITCHES=config.CBENCH_CONFIG['NUM_SWITCHES']
NUM_MACS=config.CBENCH_CONFIG['NUM_MACS']
CBENCH_WARMUP=config.CBENCH_CONFIG['CBENCH_WARMUP']
TEST_LOOP=config.CBENCH_CONFIG['TEST_LOOP']
CONTROLLER=sys.argv[1]

#my_logger_json = caplog.get_logger("CBENCH",'json')
  
##########################################################
# Cbench run with parameters imported from cbenchConf file
##########################################################

if sys.argv[2] == "-l":
   #cbench throughput mode -l
    my_logger_csv = caplog.get_logger("2-CBENCH-%s" % CONTROLLER,'csv')
    cmdcbench = 'cbench -c %s -p %s -m %s -l %s -s %s -M %s -w %s' \
    % (CONTROLLER_IP, 
       CONTROLLER_PORT, 
       MS_PER_TEST, 
       TESTS_PER_SWITCH, 
       NUM_SWITCHES, 
       NUM_MACS, 
       CBENCH_WARMUP)
elif sys.argv[2] == "-t":
   #cbench latency mode
    TEST_LOOP = 1
    my_logger_csv = caplog.get_logger("3-CBENCH-%s" % CONTROLLER,'csv')
    cmdcbench = 'cbench -c %s -p %s -m %s -l %s -s %s -M %s -w %s -t' \
    % (CONTROLLER_IP, 
       CONTROLLER_PORT, 
       MS_PER_TEST, 
       TESTS_PER_SWITCH, 
       NUM_SWITCHES, 
       NUM_MACS, 
       CBENCH_WARMUP)

print cmdcbench
print "switches;macs;avgFlowsSec"
for i in range ( TEST_LOOP ):
   print "Loop: %u" % i
   cbench=subprocess.Popen(cmdcbench, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
   (output, err) = cbench.communicate()
   cbenchResults = output[output.index('RESULT'):]
   cbenchResults = cbenchResults.replace('\n', ' ')
   switches = cbenchResults.split()[1]
   macs = NUM_MACS
   avg_num_flows = cbenchResults.split()[7].split('/')[2]
   results_csv = '%s;%s;%s' % (switches,macs,avg_num_flows)
   print results_csv
#   results_json = '{switches: %s, macs: %s, avg_num_flows: %s}' % (switches,macs,avg_num_flows)
   my_logger_csv.debug(results_csv)
#   my_logger_json.debug(results_json)
   time.sleep(5)
