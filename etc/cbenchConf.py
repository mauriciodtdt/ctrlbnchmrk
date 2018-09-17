#!/usr/bin/python

#Params for Cbench
NUM_SWITCHES="5" # Default number of switches for CBench to simulate
NUM_MACS="100"  # Default number of MACs for CBench to use
TESTS_PER_SWITCH="11"  # Default number of CBench tests to do per CBench run
MS_PER_TEST="1000"  # Default milliseconds to run each CBench test
CBENCH_WARMUP="1"  # Default number of warmup cycles to run CBench
CONTROLLER="OpenDaylight"  # Currently only support ODL
CONTROLLER_IP="localhost"  # Change this to remote IP if running on two systems
CONTROLLER_PORT="6633"  # Default port for OpenDaylight
LOOP=20 #Times that CBench will run
