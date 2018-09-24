""" 
A simple datacenter topology script for Mininet.
 
    [ s1 ]================================.
      ,---'       |           |           |
    [ s1r1 ]=.  [ s1r2 ]=.  [ s1r3 ]=.  [ s1r4 ]=.
    [ h1r1 ]-|  [ h1r2 ]-|  [ h1r3 ]-|  [ h1r4 ]-|
    [ h2r1 ]-|  [ h2r2 ]-|  [ h2r3 ]-|  [ h2r4 ]-|
    [ h3r1 ]-|  [ h3r2 ]-|  [ h3r3 ]-|  [ h3r4 ]-|
    [ h4r1 ]-'  [ h4r2 ]-'  [ h4r3 ]-'  [ h4r4 ]-'
"""
 
from mininet.topo import Topo
from mininet.util import irange



class DatacenterBasicTopo( Topo ):
    "Datacenter topology with 4 hosts per rack, 4 racks, and a root switch"
 
    def __init__(self, dpid_count):
        self.dpid_count = dpid_count
        super(DatacenterBasicTopo,self).__init__()        

    def build( self ):
        self.racks = []
        self.dpid_count += 1
        dpid = (self.dpid_count * 16) 
        rootSwitch = self.addSwitch( 's%s' % self.dpid_count, dpid = '%x' % self.dpid_count)
        for rack_num in irange( 1, 4 ):
            rack = self.buildRack( rack_num )
            self.racks.append( rack )
            for switch in rack:
                self.addLink( rootSwitch, switch )
 
    def buildRack( self, rack_num ):
        "Build a rack of hosts with a top-of-rack switch"
 
        self.dpid_count += 1
        dpid = (self.dpid_count * 16) 
        switch = self.addSwitch( 's%sr%s' % (self.dpid_count,rack_num), dpid='%x' % self.dpid_count )
 
        for host_num in irange( 1, 4 ):
            host = self.addHost( 's%sh%sr%s' % ( self.dpid_count, host_num, rack_num ) )
            self.addLink( switch, host )
 
        # Return list of top-of-rack switches for this rack
        print ("dpid: %x" %  dpid)
        print ("dpid_count: ", self.dpid_count)
        return [switch]
 
# Allows the file to be imported using `mn --custom <filename> --topo dcbasic`
#topos = {
#    'dcbasic': DatacenterBasicTopo
#}
