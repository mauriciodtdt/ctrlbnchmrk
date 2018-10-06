""" 
A simple spine leaf topology script for Mininet.
"""
 
from mininet.topo import Topo
from mininet.util import irange



class SpineLeafBasicTopo( Topo ):
 
    def __init__(self, dpid_count, spine_num, leaf_num, host_num):
        self.dpid_count = dpid_count
        self.spine_num = spine_num
        self.leaf_num = leaf_num
        self.host_num = host_num
        super(SpineLeafBasicTopo,self).__init__()

    def build( self ):
        self.spine = []
        self.leafs = []
        for s in irange( 1, self.spine_num):
           self.dpid_count += 1
           spine_switch = self.addSwitch( 's%s' % self.dpid_count, dpid = '%x' % self.dpid_count)
           self.spine.append( spine_switch )

        for s in irange( 1, self.leaf_num ):
           self.dpid_count += 1
           leaf = self.buildLeaf()
           self.leafs.append( leaf )
        "Build Links between Leaf SWs and Spine SWs"  
        for leaf_sw in self.leafs:
               for spine_sw in self.spine:
                   self.addLink( spine_sw, leaf_sw )
 
    def buildLeaf( self ):
        "Build Links between Leaf SWs and Hosts"
        leaf_switch = self.addSwitch( 'sL%s' % self.dpid_count, dpid='%x' % self.dpid_count )
 
        for h in irange( 1, self.host_num ):
            host = self.addHost( '%sh%s' % ( leaf_switch, h ) )
            self.addLink( leaf_switch, host )
        return leaf_switch
 
# Allows the file to be imported using `mn --custom <filename> --topo dcbasic`
#topos = {
#    'dcbasic': SpineLeafBasicTopo
#}
