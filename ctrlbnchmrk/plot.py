#!/usr/bin/python
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
import matplotlib.patches as mpatches
from datetime import datetime
import time

csvFile = "./tshark.log"
FMT='%H:%M:%S.%f'

data = pd.read_csv(csvFile,";")
print data.head(2)

cbench_flows = "PacketIn OFs"
cbench_time = "datetime"


#avg = data['avg_flows'].values
#stamptime = data['datetime'].values

switches = data['switchNo'].values
stamptime = data['captureTime'].values
absStamptime = []
Origin = datetime.strptime(stamptime[0][:15], FMT)
tdelta = datetime.strptime(stamptime[len(stamptime)-1][:15], FMT) - Origin
num_switches = len(stamptime)
print ("Packets: %u" % num_switches)

print ("Network Topology Time: %s" % tdelta)
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

#absstamptime = datetime.strptime(stamptime[:15], FMT) - datetime.strptime(stamptime[0][:15], FMT)
plt.gca().yaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M:%S.%f"))
plt.plot(switches,pd.to_datetime(stamptime))
#plt.plot_date(switches,absStamptime)
#plt.xticks([])
plt.figtext(.2, .8, "Time= %s" % tdelta)
plt.figtext(.2, .75, "Switches= %u" % num_switches)
plt.show()
