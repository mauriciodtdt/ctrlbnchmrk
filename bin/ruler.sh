#!/bin/bash
#Usage ./ruler <option> <sdncontroller> [PerfTest] [Topology]
#Options: -D Deploy docker-compose cbench and mininet
#         -T Run Performance Test 
#         -k Kill Docker Containers
#Performance Tests Options:
#1. Network Topology Discovery Time
#2. Asyinchronous Message Processing Time - Cbench Latency
#3. Asyinchronous Message Processing Rate - Cbench Throughput
#4. Reactive Path Provisioning Time
#5. Network Topology Change Detection Time
#6. Network Discovery Size
#7. Network Re-Provisioning Time

#####################################################
#Setting env variables CBHOME, CONTROLLER, VINTERFACE
export CBMHOME=/opt/ctrlbnchmrk
export CONTROLLER=$2
(ifconfig | grep br-) | awk 'BEGIN {FS=" "}{print $1}' > $CBMHOME/etc/docker_interface
export VINTERFACE=$(<$CBMHOME/etc/docker_interface)
#####################################################

#####################################################
#Setting test arguments
TOPOLOGY=$4 #linear | datacenter | tree | spineleaf
SWITCH_NUM=$5
HOST_NUM=$6
SCALE=$7 #Num of times to repeat same topology
#####################################################

case $1 in
#Deploy controller and services (mininet and cbench)
-D)
   echo "Deploying the environment"
   docker-compose -f /opt/ctrlbnchmrk/docker/docker-compose.yml up --no-start #&>/dev/null &
   docker-compose -f /opt/ctrlbnchmrk/docker/docker-compose.yml start mininet cbench
   docker-compose -f /opt/ctrlbnchmrk/docker/docker-compose.yml start ctrl_$2
   ;;
#Performance Tests (1 to 7) check wiki
-T)
   echo "Controller: $CONTROLLER"
   case $3 in
   "1")
      /opt/ctrlbnchmrk/ctrlbnchmrk/network_topology_discovery_13.py $TOPOLOGY $SWITCH_NUM $HOST_NUM $SCALE
      ;;
   "2")
      docker exec -it cbench python /opt/ctrlbnchmrk/ctrlbnchmrk/cbench_perf_test.py -l   
      ;;
   "3")
      docker exec -it cbench python /opt/ctrlbnchmrk/ctrlbnchmrk/cbench_perf_test.py -t
      ;;
   "4")
      ./NetworkTopologyTime.py
      ;;
   "5")
      ./NetworkTopologyTime.py
      ;;
   "6")
      ./NetworkTopologyTime.py
      ;;
   "7")
      ./NetworkTopologyTime.py
      ;;
    esac
    ;;
#Clean mininet container
-c)
   docker exec -it --privileged mininet mn -c
   ;;
#Test controller with a simple mininet linear topology
-t)
   docker exec -it --privileged mininet mn --controller=remote,ip=10.0.1.10 --topo=linear,3
   ;;
#Kill and close all containers
-k)
   docker-compose -f /opt/ctrlbnchmrk/docker/docker-compose.yml down
   ;;
-r)
   echo "do something here"
   ;;
*)
  echo $"Usage: $0 <option> <SDNCONTROLLER> [PERFORMANCE TEST] [Topology] "
  exit 1
esac

#docker run -itd --network=host --name ryu mauriciodtdt/ryu ryu ryu.app.simpe_switch
