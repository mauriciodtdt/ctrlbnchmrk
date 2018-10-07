#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
from topologies import datacenter
from topologies import spineleaf
from topologies import linear
import multiprocessing as mp
import time
import datetime
import sys

TOPOLOGY = sys.argv[1]
SCALE = int(sys.argv[2])
DPID_COUNT = int(sys.argv[3])

def build_network():
    "Bootstrap a Mininet network using the Minimal Topology"
    dpid = DPID_COUNT
    multiple_topos = []
    multiple_nets = []
    for x in range( SCALE ):
    # Create an instance of specified topology
       if TOPOLOGY == "linear":
          SWITCH_NUM = int(sys.argv[4])
          HOST_NUM = int(sys.argv[5])
          multiple_topos.append(linear.LinearBasicTopo(dpid, SWITCH_NUM,HOST_NUM))
          dpid = multiple_topos[x].dpid_count
       elif TOPOLOGY == "datacenter":
          RACK_NUM = int(sys.argv[4])
          HOST_NUM = int(sys.argv[5])
          multiple_topos.append(datacenter.DatacenterBasicTopo(dpid, RACK_NUM,HOST_NUM))
          dpid = multiple_topos[x].dpid_count
       elif TOPOLOGY == "spineleaf":
          SPINE_NUM = int(sys.argv[4])
          LEAF_NUM = int(sys.argv[5])
          HOST_NUM = int(sys.argv[6])
          multiple_topos.append(spineleaf.SpineLeafBasicTopo(dpid, SPINE_NUM, LEAF_NUM, HOST_NUM))
          dpid = multiple_topos[x].dpid_count

    # Create a network based on the topology using OVS and controlled by
    # a remote controller.
    for x in range( SCALE ):
       multiple_nets.append( Mininet(
          topo=multiple_topos[x],
          controller=lambda name: RemoteController( name, ip='10.0.1.10'),
          switch=OVSSwitch,
#         protocols=OpenFlow13,
          autoSetMacs=True ))

    print ("Wait 10 secs before start controller")
    time.sleep(10)    
    # Actually start the network
    with open ("/opt/ctrlbnchmrk/data/mininet_time_before.csv", mode='w')     as sw_file:
             sw_file.write("Time before start network(s): %s\n" % str(datetime.datetime.now()))

    for net in multiple_nets:
       net.start()

    with open ("/opt/ctrlbnchmrk/data/mininet_time_after.csv", mode='w')     as sw_file:
             sw_file.write("Time after start network(s): %s\n" % str(datetime.datetime.now()))
 
    # print "Controller Connected"
    CLI ( net )
    # Drop the user in to a CLI so user can run commands.
    
    #while True:
#    After the user exits the CLI, shutdown the network.
    
#    net.stop()
 #   net2.stop()

 
if __name__ == '__main__':
    # This runs if this file is executed directly
    setLogLevel( 'info' )
    build_network()
