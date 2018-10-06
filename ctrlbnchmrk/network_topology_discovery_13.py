#!/usr/bin/python

#The time taken by controller(s) to determine the complete network topology, 
#defined as the interval starting with the first discovery message from the 
#controller(s) at its Southbound interface, ending with all features of the 
#static topology determined.
import os
import multiprocessing as mp
import subprocess
import logging
import time
import csv
import re
import docker
import json
import sys
import lib.capture_log as caplog
import lib.docker_stats as ds
sys.path.append('/opt/ctrlbnchmrk/etc/')
import config

CBMHOME=os.environ.get("CBMHOME",None)
CONTROLLER = os.environ.get("CONTROLLER", None)
VINTERFACE = os.environ.get("VINTERFACE", None)
#SWITCH_NUM=config.MININET_CONFIG['SWITCH_NUM']
TOPOLOGY = sys.argv[1]
SWITCH_NUM = sys.argv[2]
HOST_NUM = sys.argv[3]

if TOPOLOGY == "linear":
   expected_num_links = (int(SWITCH_NUM)*2)-2
elif TOPOLOGY == "datacenter":
   expected_num_links = (int(SWITCH_NUM)*2)

print ("Topology: %s - Switches: %s - Links: %s" % (TOPOLOGY, SWITCH_NUM, expected_num_links))

OF_PORT=config.NET_TOPO_TIME['OF_PORT']
SCAN_TIME=config.NET_TOPO_TIME['SCAN_TIME']
tshark_logger_csv = caplog.get_logger("TSHARK-%s" % CONTROLLER,'csv')
docker_logger_csv = caplog.get_logger("DOCKER-%s" % CONTROLLER,'csv')
#my_logger_json = caplog.get_logger('TSHARK','json')

sw_array = {}
link_array = {}
  
def tshark_disect(q):
   #add -O to dissect packet in detail
   #cmdtshark = 'tshark -i %s -d tcp.port==%s,openflow -Y "%s" -a duration:%u' % \
#   cmdtshark = 'tshark -i %s -d tcp.port==%s,openflow -a duration:%u' % \
#    (VINTERFACE, OF_PORT, SCAN_TIME)
   cmdtshark = "tshark -q -i %s -d tcp.port==%s,openflow -V | egrep 'Arrival Time|Source Port|[Dd]atapath|In port|OFPT_FEATURES_REPLY|OFPT_PACKET_IN|Value|Chassis Subtype|Port Subtype|Reason'" % (VINTERFACE, OF_PORT)
   print cmdtshark
   link_number=0
   #output = check_output(cmd, stderr=STDOUT, timeout=seconds)
   tshark=subprocess.Popen(cmdtshark, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   #tshark=subprocess.check_output(cmdtshark)
   begin_flag = False
   PIN_flag = False
   FTRS_flag = False
   while True:
      line = tshark.stdout.readline()
      if "Arrival Time" in line:
         begin_flag = False
         PIN_flag = False
         FTRS_flag = False
         temp_timestamp = line.split()[5]
      elif "Source Port" in line:
         temp_tcp_port = line.split()[2]
      elif "OFPT_FEATURES_REPLY" in line:
         timestamp = temp_timestamp
         tcp_port = temp_tcp_port
         FTRS_flag = True
      elif re.match(r' *[Dd]atapath', line) and FTRS_flag == True:
         sw = line.split("x")[1].strip()
         sw_array[tcp_port] = [sw,timestamp]
#         print (sw,tcp_port)
      elif "OFPT_PACKET_IN" in line:
         PIN_flag = True
         timestamp = temp_timestamp
         tcp_port = temp_tcp_port
      elif re.match(r' *Reason.*(1)', line): #default 1 - if it's floodlight change for 0 - wrong reason tho
         begin_flag = True
      elif "Value" in line and begin_flag == True and PIN_flag == True:
         sw_port_in = line.split(":")[1].strip()
      elif "Chassis Subtype" in line and begin_flag == True and PIN_flag == True:
         if CONTROLLER =="ryu":
            sw_linked = line.split(":")[2].strip()
         elif CONTROLLER == "pox":
            sw_linked = line.split(":")[2].strip()
         elif CONTROLLER == "odl" or "onos":
            sw_linked = line.split("Id:")[1].strip()
#         print sw_linked
      elif "Port Subtype" in line and begin_flag == True and PIN_flag == True:
         port_linked = line.split(":")[1].strip()
         link_number += 1
#         print (port_linked)
         sw_link_left = sw_array[tcp_port][0]
         link_info = "%u;%s-%s<-->%s-%s" % (link_number,sw_link_left, sw_port_in,sw_linked,port_linked)
         tshark_logger_csv.debug(link_info)
         if not link_info in link_array:
            link_array[link_info] = timestamp
      #elif "OFPT_PACKET_OUT" in line:
      #   begin_flag = False
      
      if len(link_array) == expected_num_links:
         print ("Links: %u" % len(link_array))
         print ("Switches %u" % len(sw_array))
         

         with open ("/opt/ctrlbnchmrk/data/%s_switches.csv" % CONTROLLER, mode='w') as sw_file:
            sw_file.write("tcpport;dpid\n")
            for item in sw_array:
               sw_file.write("%s;%s\n" % (item,sw_array[item]))

         with open ("/opt/ctrlbnchmrk/data/%s_links.csv" % CONTROLLER, mode='w') as link_file:
            link_file.write("stamptime;link_number;link\n")
            for item in link_array:
               link_file.write("%s;%s\n" % (link_array[item],item))

         #print (json.dumps(link_array,indent=1))
         #print (json.dumps(sw_array,indent=1))
         q.put("TSHARK_DONE")
         break

def  docker_container_stats(q):
   while True:
      (cpu_container,mem_container) = ds.get_cpuram(CONTROLLER)
      results_csv = '%f;%u' \
       % (cpu_container,mem_container)
      docker_logger_csv.debug(results_csv)

def mininet_master(q):
   client = docker.from_env()
   container = client.containers.get("mininet")
   print container
   ### exec_run has to be tty=True and privileged
#   print container.exec_run("/opt/ctrlbnchmrk/mininet_topo_builder/mininet_master.py",tty=True, privileged=True)
#   if TOPOLOGY == "linear":
#      docker_command = "mn --controller=remote,ip=10.0.1.10 --topo=%s,%u --mac --switch=ovsk,protocols=OpenFlow13" % (TOPOLOGY, SWITCH_NUM)
#   elif TOPOLOGY == "datacenter":
   docker_command = "/opt/ctrlbnchmrk/mininet_topo_builder/mininet_master.py %s %s %s" % (TOPOLOGY, SWITCH_NUM, HOST_NUM) 
 
   print ("%s" % docker_command)
   ### exec_run has to be tty=True and privileged
   print container.exec_run(docker_command, tty=True, privileged=True) 

def main():

   q = mp.Queue()
   docker_process = mp.Process(target=docker_container_stats, args=(q,))
   tshark_process = mp.Process(target=tshark_disect, args=(q,))
   mininet_process = mp.Process(target=mininet_master, args=(q,))
   
   docker_process.daemon = True
   mininet_process.daemon = True
   tshark_process.daemon = True
   
   processes = [docker_process,tshark_process,mininet_process]

   for p in processes:
      p.start()


   while True:
      msg = q.get()
      if msg == "TSHARK_DONE":
         print "TSHARK_DONE"
         for p in processes:
            p.terminate()
         time.sleep(0.1)
         if not tshark_process.is_alive():
            tshark_process.join(timeout=1.0)
            q.close()
            break

main()
