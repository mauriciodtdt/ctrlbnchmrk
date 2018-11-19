#!/bin/bash
#Usage ./ruler <option> <sdncontroller> [PerfTest] [Topology]
#Options: -D Deploy docker-compose cbench and mininet
#         -T Run Performance Test 
#         -k Kill Docker Containers
#Performance Tests Options:
#1. Asyinchronous Message Processing Time - Cbench Latency
#2. Asyinchronous Message Processing Rate - Cbench Throughput
#3. Network Topology Discovery Time
#4. Reactive Path Provisioning Time
#5. Network Topology Change Detection Time
#6. Network Discovery Size

#####################################################
#Setting env variables CBHOME, CONTROLLER, VINTERFACE
export CBMHOME=/opt/ctrlbnchmrk
export CONTROLLER=$2
(ifconfig | grep br-) | awk 'BEGIN {FS=" "}{print $1}' > $CBMHOME/etc/docker_interface
export VINTERFACE=$(<$CBMHOME/etc/docker_interface)
#####################################################

#####################################################
#Setting test arguments
#TOPOLOGY=$4 #linear | datacenter | tree | spineleaf
#SCALE=$5 #Num of times to repeat same topology
#SWITCH_NUM=$6
#HOST_NUM=$7
#####################################################

case $1 in
#Deploy controller and services (mininet and cbench)
-D)
   echo "Deploying the environment"
   docker-compose -f /opt/ctrlbnchmrk/docker/docker-compose.yml up --no-start #&>/dev/null &
   docker-compose -f /opt/ctrlbnchmrk/docker/docker-compose.yml start mininet 
#   docker-compose -f /opt/ctrlbnchmrk/docker/docker-compose.yml start cbench
   docker-compose -f /opt/ctrlbnchmrk/docker/docker-compose.yml start ctrl_$2
   ;;
#Performance Tests (1 to 7) check wiki
-T)
   echo "Controller: $CONTROLLER"
   case $3 in
   "3")
      /opt/ctrlbnchmrk/ctrlbnchmrk/network_topology_discovery_13.py "${@:4}"
      ;;
   "1")
      docker exec -it cbench python /opt/ctrlbnchmrk/ctrlbnchmrk/cbench_perf_test.py $CONTROLLER -l   
      cp /var/lib/docker/volumes/docker_shareVolume/_data/ctrlbnchmrk/data/*CBENCH* /opt/ctrlbnchmrk/data
      ;;
   "2")
      docker exec -it cbench python /opt/ctrlbnchmrk/ctrlbnchmrk/cbench_perf_test.py $CONTROLLER -t
      cp /var/lib/docker/volumes/docker_shareVolume/_data/ctrlbnchmrk/data/*CBENCH* /opt/ctrlbnchmrk/data
      ;;
   "4")
      /opt/ctrlbnchmrk/ctrlbnchmrk/4_reactive_path_prov_time.py "${@:4}"
      ;;
   "5")
      /opt/ctrlbnchmrk/ctrlbnchmrk/5_network_topology_change_detection_time.py "${@:4}"
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
