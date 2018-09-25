""" 
A simple spine leaf topology script for Mininet.
"""
 
from mininet.topo import Topo
from mininet.util import irange



class SpineLeafBasicTopo( Topo ):
    "Datacenter topology with 4 hosts per rack, 4 racks, and a root switch"
 
    def __init__(self, dpid_count, spine_num, leaf_num, host_num):
        self.dpid_count = dpid_count
        self.spine_num = spine_num
        self.leaf_num = leaf_num
        self.host_num = host_num
        super(SpineLeafBasicTopo,self).__init__()

    def build( self ):
        self.spine = []
        self.leafs = []
        self.dpid_count += 1
        dpid = (self.dpid_count * 16) 
        for i in irange( 1, self.spine_num):
           spine_switch = self.addSwitch( 's%s' % self.dpid_count, dpid = '%x' % self.dpid_count)
           self.spine.append( spine_switch )

        for i in irange( 1, self.leaf_num ):
            leaf = self.buildLeaf( i )
            self.leafs.append( leaf )
            for leaf_sw in self.leafs:
               for spine_sw in self.spine:
                   self.addLink( spine_sw, leaf_sw )
 
    def buildLeaf( self, i ):
        "Build a rack of hosts with a top-of-rack switch"
 
        self.dpid_count += 1
        dpid = (self.dpid_count * 16) 
        leaf_switch = self.addSwitch( 's%sl%s' % (self.dpid_count,i), dpid='%x' % self.dpid_count )
 
        for j in irange( 1, self.host_num ):
            host = self.addHost( 's%sh%sl%s' % ( self.dpid_count, j, i ) )
            self.addLink( leaf_switch, host )
 
        # Return list of top-of-rack switches for this rack
        print ("dpid: %x" %  dpid)
        print ("dpid_count: ", self.dpid_count)
        return [leaf_switch]
 
# Allows the file to be imported using `mn --custom <filename> --topo dcbasic`
#topos = {
#    'dcbasic': DatacenterBasicTopo
#}
