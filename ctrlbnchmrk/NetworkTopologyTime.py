#!/usr/bin/python

#The time taken by controller(s) to determine the complete network topology, 
#defined as the interval starting with the first discovery message from the 
#controller(s) at its Southbound interface, ending with all features of the 
#static topology determined.

import multiprocessing as mp
import subprocess
import logging
import time
import re
import json
import sys
import lib.capture_log as caplog
import lib.docker_stats as ds
sys.path.append('../etc/')
import config

VINTERFACE=config.NET_TOPO_TIME['VINTERFACE']
OF_PORT=config.NET_TOPO_TIME['OF_PORT']
OFPT_FILTER=config.NET_TOPO_TIME['OFPV'] + ' == ' + str(config.NET_TOPO_TIME['OFPT_FREPLY'])
SCAN_TIME=config.NET_TOPO_TIME['SCAN_TIME']
SWITCH_NUM=config.MININET_CONFIG['SWITCH_NUM']

my_logger_csv = caplog.get_logger('TSHARK','csv')
docker_csv = caplog.get_logger('DOCKER','csv')
#my_logger_json = caplog.get_logger('TSHARK','json')
  
def tshark_disect(q):
   #add -O to dissect packet in detail
   #cmdtshark = 'tshark -i %s -d tcp.port==%s,openflow -Y "%s" -a duration:%u' % \
   cmdtshark = 'tshark -i %s -d tcp.port==%s,openflow -a duration:%u' % \
    (VINTERFACE, OF_PORT, SCAN_TIME)
   print cmdtshark
   packet_result=0
   #output = check_output(cmd, stderr=STDOUT, timeout=seconds)
   (cpu_container,mem_container)=(0,0)
   tshark=subprocess.Popen(cmdtshark, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   #tshark=subprocess.check_output(cmdtshark)
   while True:
      tsharkResults = tshark.stdout.readline()
      if tsharkResults.split()[8] == "OFPT_FEATURES_REPLY":
         packet_result += 1
         timestamp = tsharkResults.split()[1]
         typePacket = tsharkResults.split()[8]
         results_csv = '%s;%u;%s' \
          % (timestamp,packet_result,typePacket)
    #     results_json = '{timestamp: %s, switchNo: %u, typePacket: %s}' \
    #      % (timestamp, packet_result, typePacket)
         my_logger_csv.debug(results_csv)
    #     my_logger_json.debug(results_json)
      if packet_result == SWITCH_NUM:
         q.put("TSHARK_DONE")
         break

def  docker_container_stats(q):
   while True:
      (cpu_container,mem_container) = ds.get_cpuram()
      results_csv = '%f;%u' \
       % (cpu_container,mem_container)
      docker_csv.debug(results_csv)


def main():

   q = mp.Queue()
   docker_process = mp.Process(target=docker_container_stats, args=(q,))
   tshark_process = mp.Process(target=tshark_disect, args=(q,))

   docker_process.daemon = True



   processes = [docker_process,tshark_process]

   for p in processes:
      p.start()

   while True:
      msg = q.get()
      if msg == "TSHARK_DONE":
         tshark_process.terminate()
         time.sleep(0.1)
         if not tshark_process.is_alive():
            tshark_process.join(timeout=1.0)
            q.close()
            break
   

main()



