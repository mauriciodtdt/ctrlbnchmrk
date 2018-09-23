#!/usr/bin/python
import json
filepath = 'all_data2.txt'  
sw_array = {}
link_array = {}
begin_flag = False
with open(filepath) as fp:  
   line = fp.readline()
   while line:
      #print(line.strip())
      if "Arrival Time" in line:
         temp_timestamp = line.split()[5]
      elif "Source Port" in line:
         temp_tcp_port = line.split()[2]
      elif "OFPT_FEATURES_REPLY" in line:
         timestamp = temp_timestamp
         tcp_port = temp_tcp_port
      elif "Datapath" in line:
         sw = line.split("x")[1].strip()
         sw_array[tcp_port] = [sw,timestamp]
      elif "OFPT_PACKET_IN" in line:
         begin_flag = True
         timestamp = temp_timestamp
         tcp_port = temp_tcp_port
      elif "In port" in line and begin_flag == True:
         sw_port_in = line.split()[2]
      elif "dpid" in line and begin_flag == True:
         sw_linked = line.split(":")[2].strip()
      elif "Port Subtype" in line and begin_flag == True:
         port_linked = line.split(":")[1].strip()
         sw_link_left = sw_array[tcp_port][0]
         link_info = "%s-%s<-->%s-%s" % (sw_link_left, sw_port_in,sw_linked,port_linked)
         link_array[link_info] = timestamp
      elif "OFPT_PACKET_OUT" in line:
         begin_flag = False
      line = fp.readline()

print "Links: %u" % len(link_array)
print "Switches %u" % len(sw_array)
print json.dumps(link_array,indent=1)
print json.dumps(sw_array,indent=1)
