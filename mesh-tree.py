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

from my_utils import fRead
from my_utils.routeGraph import RouteGraph, NodeRank, LinkType

'''MAIN FUNCTION'''
parameters = {
                'topology': '0',
                'metric':   'srftime',
                'propagation-loss-model': 'friis',
                'tx-power': '-1',
                'protocol': 'udp',
                'data-rate': '5',
}

topoId, X, Y, Z = fRead.get_coordinates_prompt ( 1, ['n_eq_60_3d.h'], 0 )
mRouteGraph = RouteGraph (legend = parameters)
dictReport = fRead.get_csvdict_prompt (3, ['net-mp-report-001.csv'])
for nodeReport in dictReport:
    mRouteGraph.plot_node_set (nodeReport, X, Y, Z, LinkType.COMPREHENSIVE)
mRouteGraph.show_plot (mode = 'FLAT')
