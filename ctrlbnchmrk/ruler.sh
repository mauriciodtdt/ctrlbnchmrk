#!/bin/bash
#Usage ./ruler <option><sdncontroller>[PerfTest] <Perf Test Number>
#Options: -D Deploy docker-compose cbench and mininet
#         -T Run Performance Test 
#         -k Kill Docker Containers
#Performance Tests Options:
#1. cbenchPerformance Test Throughput
#2. Network Topology Discovery Time
#3.
#4.
#5.

export CONTROLLER=$2


case $1 in
-D)
   echo "Deploying the environment"
   docker-compose -f ../docker/docker-compose.yml up --no-start #&>/dev/null &
   docker-compose -f ../docker/docker-compose.yml start mininet cbench
   docker-compose -f ../docker/docker-compose.yml start ctrl_$2
   ;;
-T)
   echo "Controller: $CONTROLLER"
   case $3 in
   "1")
      docker exec -it cbench python /opt/ctrlbnchmrk/ctrlbnchmrk/cbenchPerfTest.py
      ;;
   "2")
      ./NetworkTopologyTime.py
      ;;
    esac
    ;;
-k)
   docker-compose -f ../docker/docker-compose.yml down
   ;;
-r)
   echo "do something here"
   ;;
*)
  echo $"Usage: $0 <option> <SDNCONTROLLER>[PERFORMANCE TEST]"
  exit 1
esac

#docker run -itd --network=host --name ryu mauriciodtdt/ryu ryu ryu.app.simpe_switch
