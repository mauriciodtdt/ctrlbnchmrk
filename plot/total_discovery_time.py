from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.axisartist as axisartist

x = np.arange(3)
switches = [2.074656, 1.149799, 1.166679]
links = [4.210813, 8.164355, 5.595363]
total = [5.510372, 8.272962, 5.690946]

def kilos(x, pos):
    'The two args are the value and tick position'
    return '$%1.1fK' % (x * 1e-3)


#formatter = FuncFormatter(kilos)

fig, ax = plt.subplots()
#ax.yaxis.set_major_formatter(formatter)
p1 = plt.bar(x, switches, 0.20, color='r', bottom=0)
p2 = plt.bar(x + 0.20, links, 0.20, color='b', bottom=0)
p3 = plt.bar(x + 0.40, total, 0.20, color='g', bottom=0)

plt.xticks(x, ('ONOS', 'ODL', 'RYU'),ha='left')
ax.set_title("2 Linear: 50 Switches - 1 Host\nMininet-Master")
ax.legend((p1[0],p2[0], p3[0]), ('Switches', 'Links', 'Total'))
ax.set_ylabel("Time(secs)")
ax.set_xlabel("SDN Controllers\nONOS: 5.51 - ODL: 8.27 - RYU - 5.69")
ax.autoscale_view()
plt.show()
