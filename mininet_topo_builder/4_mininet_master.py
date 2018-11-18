#!/usr/bin/python

#usage: mininet_master.py topology scale dpid_count switch host 

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
from topologies import datacenter
from topologies import spineleaf
from topologies import linear
from topologies import switches
import multiprocessing as mp
import time
import datetime
import sys


def build_network():
    TOPOLOGY = sys.argv[1]
    SCALE = int(sys.argv[2])
    DPID_COUNT = int(sys.argv[3])
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
       elif TOPOLOGY == "switches":
          SWITCH_NUM = int(sys.argv[4])
          multiple_topos.append(switches.SwitchesBasicTopo(dpid, SWITCH_NUM))
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
          controller=lambda name: RemoteController( name, ip='10.0.1.10', port=6633),
          switch=OVSSwitch,
#         protocols=OpenFlow13,
          autoSetMacs=True ))

    print ("Wait 10 secs before start controller")
    time.sleep(10)    

    for net in multiple_nets:
       net.start()
       CLI ( net )
 
if __name__ == '__main__':
    # This runs if this file is executed directly
    setLogLevel( 'info' )
    build_network()
