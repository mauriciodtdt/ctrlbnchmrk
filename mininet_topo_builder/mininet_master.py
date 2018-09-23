#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSSwitch
from topologies import datacenter
import time

def run_datacenter():
    "Bootstrap a Mininet network using the Minimal Topology"
 
    # Create an instance of our topology
    topo = datacenter.DatacenterBasicTopo()
 
    # Create a network based on the topology using OVS and controlled by
    # a remote controller.
    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController( name, ip='10.0.1.10' ),
        switch=OVSSwitch,
        autoSetMacs=True )

    print "Topology Deployed: Connect Controller?"
    
    #CLI( net )

    # Actually start the network
    net.start()
 
    print "Controller Connected"

    # Drop the user in to a CLI so user can run commands.
    CLI( net )
    #while True:
#    time.sleep(60)    
#    After the user exits the CLI, shutdown the network.
#    net.stop()
 
if __name__ == '__main__':
    # This runs if this file is executed directly
    setLogLevel( 'info' )
    run_datacenter()
