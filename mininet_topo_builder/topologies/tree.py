""" 
A simple tree topology script for Mininet.
rootSwitch
Level2Switches --> L2SWs
Level3Switches --> L3SWs per L2SW
Hosts
"""
 
from mininet.topo import Topo
from mininet.util import irange



class DatacenterBasicTopo( Topo ):
    "Datacenter topology with 4 hosts per rack, 4 racks, and a root switch"
 
    def __init__(self, dpid_count, rack_num, host_num):
        self.dpid_count = dpid_count
        self.rack_num = rack_num
        self.host_num = host_num
        super(DatacenterBasicTopo,self).__init__()        

    def build( self ):
        self.racks = []
        self.dpid_count += 1
        dpid = (self.dpid_count * 16) 
        rootSwitch = self.addSwitch( 's%s' % self.dpid_count, dpid = '%x' % self.dpid_count)
        for i in irange( 1, self.rack_num ):
            rack = self.buildRack( i )
            self.racks.append( rack )
            for switch in rack:
                self.addLink( rootSwitch, switch )
 
    def buildRack( self, i ):
        "Build a rack of hosts with a top-of-rack switch"
 
        self.dpid_count += 1
        dpid = (self.dpid_count * 16) 
        switch = self.addSwitch( 's%sr%s' % (self.dpid_count,i), dpid='%x' % self.dpid_count )
 
        for j in irange( 1, self.host_num ):
            host = self.addHost( 's%sh%sr%s' % ( self.dpid_count, j, i ) )
            self.addLink( switch, host )
 
        # Return list of top-of-rack switches for this rack
        print ("dpid: %x" %  dpid)
        print ("dpid_count: ", self.dpid_count)
        return [switch]
 
# Allows the file to be imported using `mn --custom <filename> --topo dcbasic`
#topos = {
#    'dcbasic': DatacenterBasicTopo
#}
