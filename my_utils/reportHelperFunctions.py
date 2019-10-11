'''
* Copyright (c) 2019 - 2020 Oscar Bautista
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License version 2 as published
* by the Free Software Foundation.
*
* AUTHOR: Oscar Bautista <obaut004@fiu.edu>
'''

import csv
from my_utils import fRead

def genRChangeHistogram (dstFilename, srcFilename, nNodes, dstMac, binWidth = 200):
    # Initialization of local variables
    convFactor = 1
    retransmitterDict = {}
    binStart = 0
    # Initialization of Counters per Bin
    totalRChangeCounter = 0
    rChangeCountList = [ 0 for i in range(nNodes) ]

    dictReport = fRead.get_csvdict (srcFilename)
    try:
        record = next (dictReport)
    except:
        print("No routes found, skipping generation of histogram file")
        return 0
    # Determine units of time and set convFactor variable
    timeStr = record['Time']
    timeUnit = timeStr[-2:]
    if timeUnit == 'ns':
        convFactor = 1000000
    elif timeUnit == 'us':
        convFactor = 1000
    # Process first record
    time = float(timeStr[:-2]) / convFactor
    binStart = (time // binWidth) * binWidth
    binEnd = binStart + binWidth
    node = int(record['Node'])
    # We don't care if the route change correspond to a destination different to the one with mac dstMac
    if record['Destination'] == dstMac:
        retransmitterDict[node] = record['Retransmitter']
        rChangeCountList[node] += 1
        totalRChangeCounter += 1
    # Create headers row for output csv file
    row = ['Start', 'End'] +  ['Node-{0:02d}'.format(i) for i in range (nNodes)]

    with open(dstFilename, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(row)
        for record in dictReport:
            time = float(record['Time'][:-2])/convFactor
            while time > binEnd:
                filewriter.writerow ([binStart, binEnd] + rChangeCountList)
                rChangeCountList = [ 0 for i in range(nNodes) ]
                binStart = binEnd
                binEnd = binStart + binWidth
            if record['Destination'] == dstMac:
                node = int(record['Node'])
                if (node in retransmitterDict and retransmitterDict[node] != record['Retransmitter']) or (node not in retransmitterDict):
                     retransmitterDict[node] = record['Retransmitter']
                     rChangeCountList[node] += 1
                     totalRChangeCounter += 1
        filewriter.writerow ([binStart, binEnd] + rChangeCountList)
    return totalRChangeCounter

# import fRead.def myfunc():
#     doc = "The myfunc property."
#     def fget(self):
#         return self._myfunc
#     def fset(self, value):
#         self._myfunc = value
#     def fdel(self):
#         del self._myfunc
#     return locals()
# myfunc = property(**myfunc())
