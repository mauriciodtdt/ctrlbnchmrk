#!/usr/bin/python

#The time taken by controller(s) to determine the complete network topology, 
#defined as the interval starting with the first discovery message from the 
#controller(s) at its Southbound interface, ending with all features of the 
#static topology determined.

import multiprocessing as mp
import subprocess
import logging
import re
import json
import sys
import lib.capture_log as caplog
import lib.docker_stats as ds

vInterface='docker0'
OF_Port=6633
OFPV='openflow_v1'
OFPT_Hello=0
OFPT_FRequest=5
OFPT_FReply=6
OFPT_PkIn=10
OFPT_PkOut=13
OFPT_FRemoved=11
OFPT_PStatus=12
OFPT_Filter='openflow_1_0.type == %s' % OFPT_FReply
scanTime=30

my_logger_csv = caplog.get_logger('TSHARK','csv')
#my_logger_json = caplog.get_logger('TSHARK','json')
  
#add -O to dissect packet in detail
#sudo tshark -i docker0 -d tcp.port==6633,openflow -O openflow_v1 -Y "openflow.output_port != 65531" | grep OFPT_PACKET_OUT
#cmdtshark = "tshark -i %s -d tcp.port==%s,openflow i-O %s -Y \"%s\" -a duration:10" %(vInterface,OF_Port, OFPV, OFPT_Filter)
#cmdtshark = "tshark -i %s -d tcp.port==%s,openflow -Y \"%s\" -a duration:%u > switchCount.txt" %(vInterface,OF_Port, OFPT_Filter, scanTime)
cmdtshark = 'tshark -i %s -d tcp.port==%s,openflow -Y "%s" -a duration:%u' %(vInterface,OF_Port, OFPT_Filter, scanTime)

print cmdtshark
packetCount=0

#output = check_output(cmd, stderr=STDOUT, timeout=seconds)
(cpu_container,mem_container)=(0,0)
tshark=subprocess.Popen(cmdtshark, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#tshark=subprocess.check_output(cmdtshark)

for tsharkResults in tshark.stdout.readlines():
   print (tsharkResults)
   print len(tsharkResults.split())
   if len(tsharkResults.split()) == 9:
      packetCount += 1
      timestamp = tsharkResults.split()[1]
      typePacket = tsharkResults.split()[8]
      #cpu_container = ds.get_cpu_percentage()
#      (cpu_container,mem_container) = ds.get_cpuram()
      results_csv = '%s;%u;%s;%f;%u'% (timestamp,packetCount,typePacket,cpu_container,mem_container)
 #     results_json = '{timestamp: %s, switchNo: %u, typePacket: %s}' % (timestamp, packetCount, typePacket)
      my_logger_csv.debug(results_csv)
 #     my_logger_json.debug(results_json)
      #print results_csv
#(tsharkResults, err) = tshark.communicate()
#timestamp = tsharkResults.split()[1]
#typePacket = tsharkResults.split()[12]
#avg_num_flows = tsharkResults.split()[7].split('/')[2]
#results_csv = "%s;%s" % (timestamp,typePacket)
#results_json = "{timestamp: %s, typePacket: %s}" % (timestamp, typePacket)
#my_logger_csv.debug(results_csv)
#my_logger_json.debug(results_json)

#print ( results_csv)
