from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.axisartist as axisartist

x = np.arange(5)
flowsL = [1802.2, 28335.38, 37755.46, 3416.99, 47257.7]
flowsT = [3052.9, 30094.09, 133285.65, 2986.43, 33568.73]


def kilos(x, pos):
    'The two args are the value and tick position'
    return '$%1.1fK' % (x * 1e-3)


formatter = FuncFormatter(kilos)

fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(formatter)
#p2 = plt.bar(x, flowsL, 0.35, color='r', bottom=0)
p3 = plt.bar(x, flowsT, 0.35, color='g', bottom=0)

plt.xticks(x, ('POX','ODL', 'ONOS', 'Ryu', 'Floodlight', 'OpenMUL'), ha="left")
ax.set_title("16 Switches 500 MACs\nCbench - Throughput")
#ax.legend((p2[0], p3[0]), ('Latency', 'Througput'))
ax.set_ylabel("Flows/Sec")
ax.set_xlabel("SDN Controllers")
ax.autoscale_view()
plt.show()
