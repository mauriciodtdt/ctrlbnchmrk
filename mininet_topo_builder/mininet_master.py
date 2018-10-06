#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
from topologies import datacenter
from topologies import spine_leaf
from topologies import linear
import multiprocessing as mp
import time
import sys

TOPOLOGY = sys.argv[1]
SWITCH_NUM = int(sys.argv[2])
HOST_NUM = int(sys.argv[3])


dpid_count=0

def run_datacenter():
    "Bootstrap a Mininet network using the Minimal Topology"
 
    # Create an instance of our topology
    #multiple_topos = []
    #Topology with  5 racks and 10 hosts
    if TOPOLOGY == "linear":
        topo = linear.LinearBasicTopo(dpid_count,SWITCH_NUM,HOST_NUM)
    elif TOPOLOGY == "datacenter":
        topo = datacenter.DatacenterBasicTopo(dpid_count,SWITCH_NUM,HOST_NUM)
    #Topology with 10 racks and 20 hosts
    #topo2 = datacenter.DatacenterBasicTopo(topo.dpid_count,10,20)
    #multiple_topos = [topo,topo2]


    # Create a network based on the topology using OVS and controlled by
    # a remote controller.
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController( name, ip='10.0.1.10' ),
        switch=OVSSwitch,
#        protocols=OpenFlow13,
        autoSetMacs=True )

    #net2 = Mininet(
    #    topo=topo2,
    #    controller=lambda name: RemoteController( name, ip='10.0.1.10' ),
    #    switch=OVSSwitch,
    #    autoSetMacs=True )

    #print "Topology Deployed: Connect Controller?"
    
    #CLI( net )
    print ("Wait 20 secs before start controller")
    time.sleep(20)    
    # Actually start the network
    print 
    net.start()
#    net2.start()
 
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
    run_datacenter()
