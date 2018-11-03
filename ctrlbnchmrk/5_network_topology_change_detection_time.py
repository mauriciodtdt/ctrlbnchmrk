#!/usr/bin/python
#Usage ./5 topology switches hosts (optional)

import os
import logging
import time
import subprocess
import csv
import re
import json
import sys
import lib.capture_log as caplog
sys.path.append('/opt/ctrlbnchmrk/etc/')
import config

CBMHOME=os.environ.get("CBMHOME",None)
CONTROLLER = os.environ.get("CONTROLLER", None)
VINTERFACE = os.environ.get("VINTERFACE", None)
#SRC_MAC = sys.argv[1]
#DST_MAC = sys.argv[2]
#TOPOLOGY = sys.argv[3]
'''
if TOPOLOGY == "linear":
   SWITCHES = int(sys.argv[4])
   HOSTS = int(sys.argv[5])
   expected_num_flows = (SWITCHES*2)
elif TOPOLOGY == "datacenter":
   RACKS = int(sys.argv[4])
   HOSTS = int(sys.argv[5])
   expected_num_flows = (RACKS*2)
elif TOPOLOGY == "spineleaf":
   SPINE = int(sys.argv[4])
   LEAF = int(sys.argv[5])
   HOSTS = int(sys.argv[6])
   expected_num_flows = (SPINE*2)
'''
OF_PORT=config.NET_TOPO_TIME['OF_PORT']
#tshark_logger_csv = caplog.get_logger("TSHARK-%s" % CONTROLLER,'csv')
#my_logger_json = caplog.get_logger('TSHARK','json')

prt_down_array = {}
switch_dpid_array = []
  
def tshark_disect():
   #add -O to dissect packet in detail
   cmdtshark = "tshark -q -i %s -d tcp.port==%s,openflow -V | egrep 'Epoch Time|OFPT_PORT_STATUS|OFPT_PACKET_OUT|Name|OFPPC_PORT_DOWN|Chassis Subtype'" % (VINTERFACE, OF_PORT)
   print cmdtshark
   tshark=subprocess.Popen(cmdtshark, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   begin_flag = False
   lldp_begin_flag = False
   lldp_after_failure = False
   while True:
      line = tshark.stdout.readline()
      if "Epoch Time" in line:
         begin_flag = False
         lldp_begin_flag = False
         temp_timestamp = line.split()[2]
      elif "OFPT_PORT_STATUS" in line:
         begin_flag = True
      elif "OFPT_PACKET_OUT" in line:
         lldp_begin_flag = True
      elif "Name" in line and begin_flag == True:
         switch_int = line.split()[1]
         print (switch_int) 
      elif "OFPPC_PORT_DOWN: True" in line and begin_flag == True:
         print ("Port Down")
         prt_down_timestamp = temp_timestamp
         print (prt_down_timestamp)
         prt_down_array[switch_int] = (prt_down_timestamp)
         lldp_after_failure = True  
      elif "Chassis Subtype" in line and lldp_after_failure == True and lldp_begin_flag == True:
         switch_dpid = line.split(":")[2].strip()
         switch_dpid_array.append(switch_dpid)
         print (switch_dpid)
         if '0000000000000002' in switch_dpid_array  and '0000000000000001' in switch_dpid_array:
            print ("switch_dpid_array")
            print (switch_dpid_array)
            print (temp_timestamp)
            with open ("/opt/ctrlbnchmrk/data/5_%s_change_detection.csv" % CONTROLLER, mode='w') as prt_failure_file:
               prt_failure_file.write("switch_int;timestamp\n")
               for item in prt_down_array:
                  prt_failure_file.write("%s;%s\n" % (prt_down_array[item],item))
            break

def main():

   tshark_disect()

main()
