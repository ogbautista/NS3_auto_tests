'''
* Copyright (c) 2019 - 2020 Oscar Bautista
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License version 2 as published
* by the Free Software Foundation.
*
* DESCRIPTION:
* Build a figure showing node locations and path to the root node using information collected from
* NS-3 Network Simulations.
*
* AUTHOR: Oscar Bautista <obaut004@fiu.edu>
'''

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from utils import fRead, netSimUtils

'''MAIN FUNCTION'''
LOWER_RATES = ["DsssRate1Mbps", "DsssRate2Mbps"]
MEDIUM_LOW_RATES = ["DsssRate5_5Mbps", "DsssRate11Mbps", "ErpOfdmRate6Mbps", "ErpOfdmRate9Mbps"]
MEDIUM_HIGH_RATES = ["ErpOfdmRate12Mbps", "ErpOfdmRate18Mbps", "ErpOfdmRate24Mbps"]
HIGHER_RATES = ["ErpOfdmRate36Mbps", "ErpOfdmRate48Mbps", "ErpOfdmRate54Mbps"]

topoId, X, Y, Z = fRead.get_coordinates_prompt ( 1, ['n_eq_60_3d.h'], 0 )
nNodes = len (X)

print("Building figure...")
# Aspect ratio width vs height: 0.3, figure scaling: 0.5
fig = plt.figure(figsize = plt.figaspect(0.5)*1.3)
# plt.axes().set_aspect('equal', 'datalim') # This converts the figure to 2D
fig.canvas.set_window_title('Upper View of 3D Mesh Network')
plt.subplots_adjust(left=-0.15, bottom=-0.1, right=1, top=1.05)
ax = fig.gca(projection='3d')
#ax.title.set_text( str(nNodes) + "-node topology #" + str(topoId) )
ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')

linkrate_legend = [
                Line2D([0], [0], color='b', lw=2, label='36-54  Mbps'),
                Line2D([0], [0], color='m', lw=2, label='12-24  Mbps'),
                Line2D([0], [0], color='r', lw=2, label='5.5-11 Mbps'),
                Line2D([0], [0], color='tab:orange', lw=2, label='1-2      Mbps'),
]
# Rectangle ((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
param_legend = [
                Line2D([0], [0], color='w', label = 'topology: 0' ),
                Line2D([0], [0], color='w', label = 'metric: srftime' ),
                Line2D([0], [0], color='w', label = 'propagation-loss-model: friis' ),
                Line2D([0], [0], color='w', label = 'tx-power: -1' ),
                Line2D([0], [0], color='w', label = 'protocol: udp' ),
                Line2D([0], [0], color='w', label = 'data-rate: 5' ),
]

legend1=ax.legend(handles= param_legend, handlelength= 0, handletextpad= 0, bbox_to_anchor= (0.83, 0.5 ), loc='upper left', title= 'Parameters')
#ax.legend(handles = linkrate_legend)
ax.legend(handles = linkrate_legend, bbox_to_anchor=(0.83, 0.8), loc='upper left', title= 'Link Rates')
ax.add_artist(legend1)

dictReport = fRead.get_csvdict_prompt (3, ['net-mp-report-001.csv'])

for nodeReport in dictReport:
    thisN = int(nodeReport['node'])
    if nodeReport['root']=="yes":
        ax.scatter(X[thisN], Y[thisN], Z[thisN], s=40, c='r', marker='*')
    elif nodeReport['rootNextHop'] == "ff:ff:ff:ff:ff:ff":
        ax.scatter(X[thisN], Y[thisN], Z[thisN], s=10, c='xkcd:dark gray', marker='o')
    else:
        ax.scatter(X[thisN], Y[thisN], Z[thisN], s=12, c='b', marker='o')
        nextN = int(netSimUtils.macAddr2node(nodeReport['rootNextHop']))
        color = 'xkcd:dark gray'
        lineW = 1
        for link in nodeReport['links']:
            link_noMetric = link.split(':')[0]
            link_info = link_noMetric.split('=')
            try:
                node = int(link_info[0])
            except:
                print("error during processing of link information for node", str(thisN))
                continue
            if node == nextN:
                if link_info[1] in LOWER_RATES:
                    color = 'tab:orange'
                    lineW = 1.2
                elif link_info[1] in MEDIUM_LOW_RATES:
                    color = 'r'
                elif link_info[1] in MEDIUM_HIGH_RATES:
                    color = 'm'
                    lineW = 1.1
                elif link_info[1] in HIGHER_RATES:
                    color = 'b'
        ax.plot([X[thisN], X[nextN]], [Y[thisN], Y[nextN]], [Z[thisN], Z[nextN]], color=color, linewidth=lineW)

for i in range (len (X)):
     ax.text(X[i], Y[i], Z[i], '%s' % (str(i)), size=8, zorder=1, color='k')

print("Plotting topology #{}...".format(topoId))
ax.view_init (elev=90, azim=-90)
plt.show()
print("...figure closed.")
