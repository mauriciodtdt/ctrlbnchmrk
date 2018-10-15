#!/usr/bin/python
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
import matplotlib.patches as mpatches
from datetime import datetime
import time
import sys

CONTROLLER = "odl" 
FILE=sys.argv[1]

DATA_PATH='/opt/ctrlbnchmrk/data/'

csvFileTshark = DATA_PATH +'TSHARK.csv'
#csvFileDocker = DATA_PATH +'DOCKER.csv'
FMT='%H:%M:%S.%f'

data = pd.read_csv(FILE, " ")
#docker_data = pd.read_csv(csvFileDocker,";")

print data.head(2)

#cbench_flows = "PacketIn OFs"
#cbench_time = "datetime"


#avg = data['avg_flows'].values
#stamptime = data['datetime'].values

#docker_cpu = docker_data['cpu'].values
#docker_time = docker_data['time'].values
switches = np.arange(100)
#links = data['link_number'].values
stamptime = data['stamptime'].values

#docker_data = pd.read_csv(csvFile,";"


absStamptime = []
Origin = datetime.strptime(stamptime[0][:15], FMT)
tdelta = datetime.strptime(stamptime[len(stamptime)-1][:15], FMT) - Origin
num_switches = len(stamptime)
print ("Switches: %u" % num_switches)

print ("Network Topology Time: %s" % tdelta)

'''
for x in stamptime:
   New = datetime.strptime(x[:15], FMT)
#   print New
   absTime = (str(New-Origin))
#   print absTime
#   print type(absTime)
   if absTime=='0:00:00':
      absStamptime.append (['0:00:00.000001'])
   else:
      absStamptime.append ([absTime])
'''
#plt.figure(1)
#plt.plot(pd.to_datetime(docker_time),docker_cpu)
#plt.legend("docker cpu")
#plt.figure(2)
fig, ax = plt.subplots()
ax.set_title("ODL - Switches Discovery Time\n\
   Topology: Linear\n\
   Scale:2 Switches: 50 Hosts: 1")
ax.set_ylabel("Switches")
ax.set_xlabel("Time")
plt.plot_date(pd.to_datetime(stamptime),switches)
#plt.plot_date(switches,absStamptime)
plt.xticks(rotation=45)
plt.figtext(.2, .8, "Time= %s" % tdelta)
plt.figtext(.2, .75, "Switches= %u" % num_switches)
ax.autoscale_view()
plt.show()
