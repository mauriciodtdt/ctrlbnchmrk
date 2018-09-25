#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
from topologies import datacenter
from topologies import spine_leaf
import multiprocessing as mp
import time

dpid_count=0

def run_datacenter():
    "Bootstrap a Mininet network using the Minimal Topology"
 
    # Create an instance of our topology
    #multiple_topos = []
    #Topology with  4 spines 8 leafs and 10 hosts
    topo = spine_leaf.SpineLeafBasicTopo(dpid_count,4,8,10)
    #Topology with 10 racks and 20 hosts
    #topo2 = datacenter.DatacenterBasicTopo(topo.dpid_count,10,20)
    #multiple_topos = [topo,topo2]


    # Create a network based on the topology using OVS and controlled by
    # a remote controller.
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController( name, ip='127.0.0.1' ),
        switch=OVSSwitch,
        autoSetMacs=True )

    #net2 = Mininet(
     #   topo=topo2,
      #  controller=lambda name: RemoteController( name, ip='127.0.0.1' ),
      #  switch=OVSSwitch,
       # autoSetMacs=True )

    #print "Topology Deployed: Connect Controller?"
    
    #CLI( net )

    # Actually start the network
    net.start()
    time.sleep(60)    
    #net2.start()
 
    # print "Controller Connected"
    #CLI ( net )
    # Drop the user in to a CLI so user can run commands.
    
    #while True:
#    After the user exits the CLI, shutdown the network.
    
    net.stop()
    #net2.stop()
 
if __name__ == '__main__':
    # This runs if this file is executed directly
    setLogLevel( 'info' )
    run_datacenter()
