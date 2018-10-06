""" 
A simple linear topology script for Mininet.
"""
 
from mininet.topo import Topo
from mininet.util import irange



class LinearBasicTopo( Topo ):
    "Topology for a string of N hosts and N-1 switches."
 
    def __init__(self, dpid_count, switch_num, host_num):
        self.dpid_count = dpid_count
        self.switch_num = switch_num
        self.host_num = host_num
        super(LinearBasicTopo,self).__init__()        

    def build( self ):
       self.total_sws = []
       "Build Switches" 
       for s in irange (1, self.switch_num):
          self.dpid_count += 1
          switch = self.buildHostLinks()
          self.total_sws.append(switch)
       last = None 
       "Build Links between Switches"
       for sw in self.total_sws:
          if last:
             self.addLink( last, sw)
          last = sw


        # Wire up switches
    def buildHostLinks ( self ):
       "Build Links between Switches and Hosts"
       switch = self.addSwitch( 's%s' % self.dpid_count, dpid = '%x' % self.dpid_count )
       for h in irange ( 1, self.host_num ):
          host = self.addHost( '%sh%s' % ( switch, h ) )
          self.addLink( switch, host )
       return switch
 
# Allows the file to be imported using `mn --custom <filename> --topo dcbasic`
#topos = {
#    'dcbasic': LinearBasicTopo
#}
