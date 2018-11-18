#!/usr/bin/python
#Usage ./4 source_mac dest_mac topology switches hosts (optional)

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
SRC_MAC = sys.argv[1]
DST_MAC = sys.argv[2]
TOPOLOGY = sys.argv[3]

if TOPOLOGY == "linear":
   SWITCHES = int(sys.argv[4])
   HOSTS = int(sys.argv[5])
   expected_num_flows = (SWITCHES*2)
   print (expected_num_flows)
elif TOPOLOGY == "datacenter":
   RACKS = int(sys.argv[4])
   HOSTS = int(sys.argv[5])
   expected_num_flows = (RACKS*2)
elif TOPOLOGY == "spineleaf":
   SPINE = int(sys.argv[4])
   LEAF = int(sys.argv[5])
   HOSTS = int(sys.argv[6])
   expected_num_flows = (SPINE*2)

OF_PORT=config.NET_TOPO_TIME['OF_PORT']
SCAN_TIME=config.NET_TOPO_TIME['SCAN_TIME']
#tshark_logger_csv = caplog.get_logger("TSHARK-%s" % CONTROLLER,'csv')
#my_logger_json = caplog.get_logger('TSHARK','json')

  
def tshark_disect():
   dst_flow_array = []
   src_flow_array = []
   arp_timestamp = ""
   #add -O to dissect packet in detail
   cmdtshark = "tshark -q -i %s -d tcp.port==%s,openflow -V | egrep 'Epoch Time|OFPT_FLOW_MOD|OFPFC_ADD|OFPXMT_OFB_IN_PORT|OFPXMT_OFB_ETH_(SRC|DST)|Value|ARP|Target IP address'" % (VINTERFACE, OF_PORT)
   print cmdtshark
   tshark=subprocess.Popen(cmdtshark, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   begin_flag = False
   DST_flag = False
   SRC_flag = False
   ARP_flag = True
   
   while True:
      line = tshark.stdout.readline()
      if "Epoch Time" in line:
         begin_flag = False
         DST_flag = False
         SRC_flag = False
         temp_timestamp = line.split()[2]
      elif "Target IP address: 10.0.0.100" in line and ARP_flag == True:
         arp_timestamp = temp_timestamp
         ARP_flag = False
      elif "OFPFC_ADD" in line:
         begin_flag = True
         timestamp = temp_timestamp
      elif "OFPXMT_OFB_ETH_DST" in line:
         DST_flag = True
         SRC_flag = False
      elif "OFPXMT_OFB_ETH_SRC" in line:
         SRC_flag = True
         DST_flag = False
      elif "Value" in line and DST_flag == True:
         if DST_MAC in line:
            dst_flow_array.append(timestamp)
#            print ("dst %s" % timestamp)
            print ("lenght dest: %u" % len(dst_flow_array))
         if SRC_MAC in line:
            src_flow_array.append(timestamp)
#            print ("src %s" % timestamp)
            print ("lenght src: %u" % len(src_flow_array))
      if (len(src_flow_array) + len(dst_flow_array)) == expected_num_flows:
         
         with open ("/opt/ctrlbnchmrk/data/%s_flows.csv" % CONTROLLER, mode='w') as flow_file:
            flow_file.write("timestamp;flow_number;flow_dir\n")
            for item in dst_flow_array:
               flow_file.write("%s;%u;dst\n" % (item,dst_flow_array.index(item)))
            for item in src_flow_array:
               flow_file.write("%s;%u;src\n" % (item,src_flow_array.index(item)))

         #1. controller get the arp request from source and broadcast it to all
         #the switches
         print ("initial arp request at: %s" % arp_timestamp)
         #2. controller get the arp reply from destination and setup the path
         #from destination to source
         print ("last added flow to reach back the source at: %s" % src_flow_array[-1])      
         #3. cotroller get the icmp request from source and setup the path from source 
         #to destination
         print ("last added flow to reach destination at: %s" % dst_flow_array[-1])
       
         break
def main():

   tshark_disect()

main()
