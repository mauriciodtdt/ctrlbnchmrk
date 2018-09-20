import time
import docker
import json
import datetime

cli=docker.from_env()
client = docker.APIClient(base_url='unix://var/run/docker.sock')

def get_stats(CONTROLLER):
   cli=client.stats(container=CONTROLLER,decode=True, stream=False)
   return json.dumps(cli,indent=1)

#def get_cpu_percentage():
def get_cpuram(CONTROLLER):
   cli=client.stats(container=CONTROLLER,decode=True, stream=False)
   cpu_percentage=0
   container_delta = cli['cpu_stats']['cpu_usage']['total_usage'] \
    - cli['precpu_stats']['cpu_usage']['total_usage']
   host_delta = cli['cpu_stats']['system_cpu_usage'] \
    - cli['precpu_stats']['system_cpu_usage']
   percpu_usage = len(cli['cpu_stats']['cpu_usage']['percpu_usage'])
#   percpu_usage = 1
   if host_delta > 0 and container_delta > 0:
      cpu_percentage = (float(container_delta)/float(host_delta))*percpu_usage*100
      # * cli['cpu_stats']['cpu_usage']['percpu_usage']
   mem = (cli['memory_stats']['usage'] - cli['memory_stats']['stats']['cache'])/1048576
   return (cpu_percentage,mem)

def get_ram(CONTROLLER):
   cli=client.stats(container=CONTROLLER,decode=True, stream=False)
   mem = (cli['memory_stats']['usage'] - cli['memory_stats']['stats']['cache'])/1048576
   return mem

#while True:
#   print get_cpuram()
#   time.sleep(1)
