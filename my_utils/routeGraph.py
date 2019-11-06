'''
* Copyright (c) 2019 - 2020 Oscar Bautista
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License version 2 as published
* by the Free Software Foundation.
*
* DESCRIPTION:
* Class RouteGraph the represent nodes and the links between them with colors.
*
* AUTHOR: Oscar Bautista <obaut004@fiu.edu>
'''
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from enum import Enum
from my_utils import netSimUtils

class NodeRank (Enum):
    ROOT = 1
    TRANSMITTING = 2
    SILENT = 3
    NOROOTPATH = 4
    ISOLATED = 5

class LinkType (Enum):
    ALL = 1
    ROOTPATH = 2
    PEER = 3
    COMPREHENSIVE = 4
    NONE = 5

class RouteGraph:
    _LOWER_RATES = ["DsssRate1Mbps", "DsssRate2Mbps"]
    _MEDIUM_LOW_RATES = ["DsssRate5_5Mbps", "DsssRate11Mbps", "OfdmRate6Mbps", "ErpOfdmRate6Mbps", "OfdmRate9Mbps", "ErpOfdmRate9Mbps"]
    _MEDIUM_HIGH_RATES = ["OfdmRate12Mbps", "ErpOfdmRate12Mbps", "OfdmRate18Mbps", "ErpOfdmRate18Mbps", "OfdmRate24Mbps", "ErpOfdmRate24Mbps"]
    _HIGHER_RATES = ["OfdmRate36Mbps", "ErpOfdmRate36Mbps", "OfdmRate48Mbps", "ErpOfdmRate48Mbps", "OfdmRate54Mbps", "ErpOfdmRate54Mbps"]

    def __init__ (self, legend, fTitle = None, dimension= '3d'):
        self._legendDict = legend
        self._dimension = dimension
        print("Building figure...")
        # figaspect set the relation height/width, the multiplier scales the whole figure
        fig = plt.figure(figsize = plt.figaspect(0.5)*1.3)
            # *** Alternative, grid modification does not work ***
            # fig, ax = plt.subplots(figsize = plt.figaspect(0.5)*1.3)
            # ax.grid(linestyle='-', linewidth='0.5', color='red')
        # Set title for the Figure
        if fTitle is None:
            if dimension == '3d':
                fTitle = 'Upper View of 3D Mesh Network'
            elif dimension == '2d':
                fTitle = '2D Mesh Network'
        fig.canvas.set_window_title(fTitle)
        self._axes = fig.gca(projection= dimension)
        # Set axes labels
        self._axes.set_xlabel ('x axis')
        self._axes.set_ylabel ('y axis')
        self._axes.set_zlabel ('z axis')

    def display_legend (self, mode = 'DEFAULT'):
        param_legend_list = []
        for key, value in self._legendDict.items():
            label = str(key) + ': ' + str(value)
            legendEntry = Line2D([0], [0], color='w', label = label)
            param_legend_list.append(legendEntry)

        linkrate_legend_list = [
                        Line2D([0], [0], color='b', lw=2, label='36-54  Mbps'),
                        Line2D([0], [0], color='m', lw=2, label='12-24  Mbps'),
                        Line2D([0], [0], color='r', lw=2, label='5.5-11 Mbps'),
                        Line2D([0], [0], color='tab:orange', lw=2, label='1-2      Mbps'),
                        ]
        if mode == 'FLAT':
            param_legend = self._axes.legend (handles= param_legend_list, handlelength= 0, handletextpad= 0, bbox_to_anchor= (0.82, 0.5 ), loc='upper left', title= 'Parameters')
            self._axes.legend(handles = linkrate_legend_list, bbox_to_anchor=(0.82, 0.8), loc='upper left', title= 'Link Rates')
        else:
            param_legend = self._axes.legend (handles= param_legend_list, handlelength= 0, handletextpad= 0, bbox_to_anchor= (0.93, 0.5 ), loc='upper left', title= 'Parameters')
            self._axes.legend(handles = linkrate_legend_list, bbox_to_anchor=(0.93, 0.8), loc='upper left', title= 'Link Rates')
        self._axes.add_artist(param_legend)

    def plot_node (self, X, Y, Z= 0, nodeRank=NodeRank.TRANSMITTING):
        if nodeRank == NodeRank.ROOT:
            self._axes.scatter(X, Y, Z, s=50, c='xkcd:light gray', marker = 'o', linewidths=0.7, edgecolor='b')
            self._axes.scatter(X, Y, Z, s=25, c='r', marker='*')
        elif nodeRank == NodeRank.NOROOTPATH:
            self._axes.scatter(X, Y, Z, s=10, c='xkcd:dark gray', marker='o')
        elif nodeRank == NodeRank.SILENT:
            self._axes.scatter(X, Y, Z, s=20, c='k', marker='o')
            self._axes.scatter(X, Y, Z, s=12, c='r', marker='2')
        elif nodeRank == NodeRank.TRANSMITTING:
            self._axes.scatter(X, Y, Z, s=12, c='b', marker='o')

    def plot_node_set (self, nodeInfo, X, Y, Z = [ ] , linkType = LinkType.COMPREHENSIVE, labels = True):
        showRootLink = False
        if linkType == LinkType.ALL or linkType == LinkType.ROOTPATH or linkType == LinkType.COMPREHENSIVE:
            showRootLink = True
        showPeerLink = False
        if linkType == LinkType.ALL or linkType == LinkType.PEER:
            showPeerLink = True
        sn = int(nodeInfo['node'])
        rootdn = None
        if  nodeInfo['root']=="yes":
            self.plot_node (X[sn], Y[sn], Z[sn], NodeRank.ROOT)
        elif nodeInfo['rootNextHop'] == "ff:ff:ff:ff:ff:ff":
            self.plot_node (X[sn], Y[sn], Z[sn], NodeRank.NOROOTPATH)
            if linkType == LinkType.COMPREHENSIVE:
                showPeerLink = True
        elif nodeInfo['TxUnicastData'] == '0':
            self.plot_node (X[sn], Y[sn], Z[sn], NodeRank.SILENT)
            rootdn = int(netSimUtils.macAddr2node(nodeInfo['rootNextHop']))
        else:
            self.plot_node (X[sn], Y[sn], Z[sn], NodeRank.TRANSMITTING)
            rootdn = int(netSimUtils.macAddr2node(nodeInfo['rootNextHop']))
        # print node label
        if labels:
            self._axes.text(X[sn]+5, Y[sn]+5, Z[sn], '%s' % (str(sn)), size=8, zorder=1, color='k')
        # key 'links' exist only when there is at least one peer link
        if linkType != LinkType.NONE and 'links' in nodeInfo.keys():
            for link in nodeInfo['links']:
                link_noMetric = link.split(':')[0]
                link_phy = link_noMetric.split('=')
                try:
                    dn = int(link_phy[0])
                except:
                    print("error during processing of link information for node", str(sn))
                    continue
                if showRootLink and dn == rootdn:
                    self.plot_root_link ( link_phy[1], [X[sn], X[dn]], [Y[sn], Y[dn]], [Z[sn], Z[dn]] )
                elif showPeerLink and dn > sn: # dn > sn ensures that each link is only drawn once
                    self.plot_peer_link ( [X[sn], X[dn]], [Y[sn], Y[dn]], [Z[sn], Z[dn]] )

    def plot_root_link (self, linkRate, Xp, Yp, Zp = [0, 0]):
        color = 'xkcd:dark gray'
        lineW = 1
        if linkRate in self._LOWER_RATES:
            color = 'tab:orange'
            lineW = 1.2
        elif linkRate in self._MEDIUM_LOW_RATES:
            color = 'r'
        elif linkRate in self._MEDIUM_HIGH_RATES:
            color = 'm'
            lineW = 1.1
        elif linkRate in self._HIGHER_RATES:
            color = 'b'
        self._axes.plot(Xp, Yp, Zp, color=color, linewidth=lineW)

    def plot_peer_link (self, Xp, Yp, Zp = [0,0]):
        color = 'xkcd:dark gray'
        lineW = 0.5
        self._axes.plot(Xp, Yp, Zp, color=color, linewidth=lineW)

    def plot_node_labels (self, X, Y, Z):
        for i in range (len (X)):
            self._axes.text(X[i], Y[i], Z[i], '%s' % (str(i)), size=8, zorder=1, color='k')

    def show_plot (self, mode = 'DEFAULT'):
        self.display_legend (mode)
        print("Showing figure...")
        if mode == 'FLAT':
            plt.subplots_adjust(left= -0.15, bottom= -0.1, right= 1, top= 1.05)
            self._axes.view_init (elev= 90, azim= -90)
        else:
            plt.subplots_adjust(left= -0.1, bottom= -0.0, right= .87, top= 1)
        plt.show()
        print("...figure closed.")
