# config.py
# Contains configuration for the testing environment, cbench, mininet
# and wireshark.

CONF = {
   'CONTROLLER': "SDNCONTROLLER", # Currently only support ODL
   'CONTROLLER_IP': '10.0.1.10', # Change this to remote IP if running on two systems
   'CONTROLLER_PORT': '6633' # Default port for OpenDaylight
}


CBENCH_CONFIG = {
   'NUM_SWITCHES': '5', # Default number of switches for CBench to simulate
   'NUM_MACS': '100', # Default number of MACs for CBench to use
   'TESTS_PER_SWITCH': '4', # Default (11) number of CBench tests to do per CBench run
   'MS_PER_TEST': '500', # Default milliseconds to run each CBench test
   'CBENCH_WARMUP': '1', # Default number of warmup cycles to run CBench
   'TEST_LOOP': 3 #Times that CBench will run
}

NET_TOPO_TIME = {
   'OF_PORT': 6633,
   'OFPV': 'openflow_1_0.type',
   'OFPT_HELLO': 0,
   'OFPT_FREQUEST': 5,
   'OFPT_FREPLY': 6,
   'OFPT_PKIN': 10,
   'OFPT_PKOUT': 13,
   'OFPT_FREMOVED': 11,
   'OFPT_PSTATUS': 12,
   'SCAN_TIME': 300
}

MININET_CONFIG = {
   'SWITCH_NUM': 100
}
