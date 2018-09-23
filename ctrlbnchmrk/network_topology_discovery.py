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
#CONTROLLER = "ryu"
VINTERFACE = os.environ.get("VINTERFACE", None)


OF_PORT=config.NET_TOPO_TIME['OF_PORT']
OFPT_FILTER=config.NET_TOPO_TIME['OFPV'] + ' == ' + str(config.NET_TOPO_TIME['OFPT_FREPLY'])
SCAN_TIME=config.NET_TOPO_TIME['SCAN_TIME']
SWITCH_NUM=config.MININET_CONFIG['SWITCH_NUM']
print SWITCH_NUM
my_logger_csv = caplog.get_logger('TSHARK','csv')
docker_csv = caplog.get_logger('DOCKER','csv')
#my_logger_json = caplog.get_logger('TSHARK','json')

sw_array = {}
link_array = {}
  
def tshark_disect(q):
   #add -O to dissect packet in detail
   #cmdtshark = 'tshark -i %s -d tcp.port==%s,openflow -Y "%s" -a duration:%u' % \
#   cmdtshark = 'tshark -i %s -d tcp.port==%s,openflow -a duration:%u' % \
#    (VINTERFACE, OF_PORT, SCAN_TIME)
   cmdtshark = "tshark -q -i %s -d tcp.port==%s,openflow -V \
    | egrep 'Arrival Time|Source Port|ID|In port|OFPT_FEATURES_REPLY|PACKET_(IN|OUT)|dpid|Port component|Reason'" \
    % (VINTERFACE, OF_PORT)
   print cmdtshark
   #packet_result=0
   #output = check_output(cmd, stderr=STDOUT, timeout=seconds)
   tshark=subprocess.Popen(cmdtshark, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   #tshark=subprocess.check_output(cmdtshark)
   begin_flag = False
   PIN_flag = False
   while True:
      line = tshark.stdout.readline()
      if "Arrival Time" in line:
         begin_flag = False
         PIN_flag = False
         temp_timestamp = line.split()[5]
      elif "Source Port" in line:
         temp_tcp_port = line.split()[2]
      elif "OFPT_FEATURES_REPLY" in line:
         timestamp = temp_timestamp
         tcp_port = temp_tcp_port
      elif "Datapath" in line:
         sw = line.split("x")[1].strip()
         sw_array[tcp_port] = [sw,timestamp]
#         print (sw,tcp_port)
      elif "OFPT_PACKET_IN" in line:
         PIN_flag = True
         timestamp = temp_timestamp
         tcp_port = temp_tcp_port
      elif "In port" in line and PIN_flag == True:
         sw_port_in = line.split()[2]
      elif "Reason: Action explicitly output to controller (1)" in line:
         begin_flag = True
      elif "dpid" in line and begin_flag == True:
         sw_linked = line.split(":")[2].strip()
      elif "Port Subtype" in line and begin_flag == True:
         port_linked = line.split(":")[1].strip()
 #        print (tcp_port)
         sw_link_left = sw_array[tcp_port][0]
         link_info = "%s-%s<-->%s-%s" % (sw_link_left, sw_port_in,sw_linked,port_linked)
         my_logger_csv.debug(link_info)
         link_array[link_info] = timestamp
      elif "OFPT_PACKET_OUT" in line:
         begin_flag = False

      if len(link_array) == ((SWITCH_NUM*2)-2):
         print ("Links: %u" % len(link_array))
         print ("Switches %u" % len(sw_array))
#         print (json.dumps(link_array,indent=1))
#         print (json.dumps(sw_array,indent=1))
#         print "inside the if"
         q.put("TSHARK_DONE")
         break

def  docker_container_stats(q):
   while True:
      (cpu_container,mem_container) = ds.get_cpuram(CONTROLLER)
      results_csv = '%f;%u' \
       % (cpu_container,mem_container)
      docker_csv.debug(results_csv)

def mininet_master(q):
   client = docker.from_env()
   container = client.containers.get("mininet")
   print container
   #print container.exec_run("/opt/ctrlbnchmrk/mininet_topo_builder/mininet_master.py",tty=False, privileged=True)
   print container.exec_run("mn --controller=remote,ip=10.0.1.10 --topo=linear,50", tty=True, privileged=True)
   
def main():

   q = mp.Queue()
   docker_process = mp.Process(target=docker_container_stats, args=(q,))
   tshark_process = mp.Process(target=tshark_disect, args=(q,))
   mininet_process = mp.Process(target=mininet_master, args=(q,))
   
   docker_process.daemon = True
   mininet_process.daemon = True
   processes = [docker_process,tshark_process,mininet_process]

   for p in processes:
      p.start()


   while True:
      msg = q.get()
      if msg == "TSHARK_DONE":
         print "TSHARK_DONE"
         tshark_process.terminate()
         time.sleep(0.1)
         if not tshark_process.is_alive():
            tshark_process.join(timeout=1.0)
            q.close()
            break
   
   for p in processes:
      p.stop()

main()
