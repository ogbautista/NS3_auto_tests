'''
* Copyright (c) 2019 - 2020 Oscar Bautista
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License version 2 as published
* by the Free Software Foundation.
*
* DESCRIPTION:
* Utility program to run a number of NS-3 simulation tests continuously and parse xml result files to record
* the data of interestand summarize in csv files.
*
* AUTHOR: Oscar Bautista <obaut004@fiu.edu>
'''
'''
Next features:
Add a command line option to redo specific tests that contain specific parameter values
Future Fixes:
Flows are numbered in the order the application starts (headings), but the stats are ordered in ascending flow number (content)
'''

import os, sys
import xml.etree.ElementTree as ET
import csv
from copy import deepcopy
from my_utils.reportHelperFunctions import genRChangeHistogram

'LIMITATIONS'
'For all the simulation tests the number of nodes in the network should be the same, and it requires to be set in the "testPar" dictionary below'

# By default execute tests at TEST_LIST instead of combination of parameters values specified at param_set
# In other words, this program will run one or the other not both
runList = True
# If test was interrupted, this allows to continue from the point it was stopped by skipping completed tests
skip = 0
# test index options for report file names, used when replacing specific simulation tests run in a previous batch
test_iter_offset = 0
test_iter_increment = 1
# List of tests to run, arguments and values only, areguments don't need to be preceded by "--"
TEST_LIST = [
            "--tx-power=2.0 --remote-station-manager=arf --wifi-standard=80211g --propagation-loss-model=friis --protocol=udp --airtime-b=true --root=00:00:00:00:00:10 --do-flag=true",
            "--tx-power=3.0 --remote-station-manager=arf --wifi-standard=80211g --propagation-loss-model=friis --protocol=udp --airtime-b=true --root=00:00:00:00:00:10 --do-flag=true",
            "--tx-power=4.0 --remote-station-manager=arf --wifi-standard=80211g --propagation-loss-model=friis --protocol=udp --airtime-b=true --root=00:00:00:00:00:10 --do-flag=true",
            "--tx-power=2.0 --remote-station-manager=minstrelht --wifi-standard=80211n2.4 --propagation-loss-model=friis --protocol=udp --airtime-b=true --root=00:00:00:00:00:10 --do-flag=true",
            "--tx-power=3.0 --remote-station-manager=minstrelht --wifi-standard=80211n2.4 --propagation-loss-model=friis --protocol=udp --airtime-b=true --root=00:00:00:00:00:10 --do-flag=true",
            "--tx-power=4.0 --remote-station-manager=minstrelht --wifi-standard=80211n2.4 --propagation-loss-model=friis --protocol=udp --airtime-b=true --root=00:00:00:00:00:10 --do-flag=true",
            "--tx-power=-6.0 --remote-station-manager=arf --wifi-standard=80211g --propagation-loss-model=itur1411 --protocol=tcp --airtime-b=true --root=ff:ff:ff:ff:ff:ff --do-flag=false",
            "--tx-power=-5.0 --remote-station-manager=arf --wifi-standard=80211g --propagation-loss-model=itur1411 --protocol=tcp --airtime-b=true --root=ff:ff:ff:ff:ff:ff --do-flag=false",
            "--tx-power=-4.0 --remote-station-manager=arf --wifi-standard=80211g --propagation-loss-model=itur1411 --protocol=tcp --airtime-b=true --root=ff:ff:ff:ff:ff:ff --do-flag=false",
            "--tx-power=-6.0 --remote-station-manager=minstrelht --wifi-standard=80211n2.4 --propagation-loss-model=itur1411 --protocol=tcp --airtime-b=true --root=ff:ff:ff:ff:ff:ff --do-flag=false",
            "--tx-power=-5.0 --remote-station-manager=minstrelht --wifi-standard=80211n2.4 --propagation-loss-model=itur1411 --protocol=tcp --airtime-b=true --root=ff:ff:ff:ff:ff:ff --do-flag=false",
            "--tx-power=-4.0 --remote-station-manager=minstrelht --wifi-standard=80211n2.4 --propagation-loss-model=itur1411 --protocol=tcp --airtime-b=true --root=ff:ff:ff:ff:ff:ff --do-flag=false"
]
param_set = [
            {
            #"wp-mobility" : ["true"],
            "topology" : [],
            "metric": ["srftime"],# "airtime", "airtime-b", "etx", "hop-count"], #"pckatime-srb1", "fdpow2", #srptime-efp2 #pckatime-srb1 is same srftime (renamed)
            "propagation-loss-model" : ["friis"],
            "tx-power" : ["-1", "0"],
            "protocol" : ["udp", "tcp"],
            "data-rate" : ["5", "10", "20"],
            #"metric-distance-mode" : ["0",],
            #"leap-seconds": ["0",],
            },
            {
            #"wp-mobility" : ["true"],
            "topology" : [],
            "metric": ["srftime"],
            "propagation-loss-model" : ["itur1411"],
            "tx-power" : ["-5", "-4"],
            "protocol" : ["udp", "tcp"],
            "data-rate" : ["5", "10", "20"],
            },
            # {
            # "wp-mobility" : ["true"],
            # "topology" : ["1"],
            # "metric": ["srftime", "airtime", "airtime-b", "etx", "hop-count"], #"pckatime-srb1", "fdpow2", #srptime-efp2 #pckatime-srb1 is same srftime (renamed)
            # "propagation-loss-model" : ["itur1411NLos"],
            # "tx-power" : ["1", "2", "3"],
            # "protocol" : ["udp", "tcp"],
            # "data-rate" : ["5", "10", "20"],
            # },
            # {
            # "topology" : [],
            # "data-rate" : ["5", "10", "20"],
            # "metric": ["airtime"],
            # "protocol" : ["udp"],
            # "propagation-loss-model" : ["friis"],
            # "tx-power" : ["0"]
            # }
]
for i in range (30):
    param_set[0]['topology'].append( str(i) )
    param_set[1]['topology'].append( str(i) )

destinationIP = "10.1.1.1"  # Ip Address for sink node for which statistics is to be collected
destinationMAC = "00:00:00:00:00:01" # MAC address of sink node (Typically the root node)
testFileName = "mymesh"     # ns3-test filename
flowMonReportFile = 'MyMeshPerformance.xml' # Flow monitor report file name
mpReportBaseName = 'mp-report-'
dataReportFilename = 'testSummary-60Nodes-oscarlaptop-srftime-friis-itur1411.csv' #2NewStaticMetrics, srptime-efp2
mpSummaryReportBaseName = 'net-mp-report-'
logRouteChanges = True
rChangesReportFilename = 'rChanges.csv'
rChangeHstgBaseName = 'rChangeHistogram-'

physicalPar = {
            "EnergyDetectionThreshold": -87.0,
            "CcaMode1Threshold": -99.0,
            "TxGain": 0.0,
            "RxGain": 0.0,
            "tx-power": 0.0,
            "RxNoiseFigure": 7.0,
            "Antennas": 2,
            "remote-station-manager": "minstrelht",
            "wifi-standard": "80211n2.4",
            "GreenfieldEnabled": False,
            "MaxSupportedTxSpatialStreams": 1,
            "MaxSupportedRxSpatialStreams": 1,
            "ShortGuardEnabled": False,
}
networkPar = {
            "start": 0.2,
            "MaxBeaconLoss": 10,
            "MaxRetries": 4,
            "MaxPacketFailure": 5,
            "Dot11MeshHWMPnetDiameterTraversalTime": 0.4096,
            "Dot11MeshHWMPactivePathTimeout": 5.12,
            "Dot11MeshHWMPactiveRootTimeout": 5.12,
            "Dot11MeshHWMPmaxPREQretries": 3,
            "UnicastPreqThreshold": 1,
            "UnicastDataThreshold": 1,
            "do-flag": True,
            "rf-flag": True,
            "root": "00:00:00:00:00:01",
            "metric": "airtime",
            "beacon-window": 30,
}
testPar = {
            "x-size": 3,
            "y-size": 3,
            "step": 100.0,
            "grid": False,
            "nodes":  60,
            "topology": 0,
            "packet-start": 3.0,
            "time": 103.0,
            "packet-size": 536,
            "data-rate": 50,
            "interfaces": 1,
            "channels": True,
            "protocol": "udp",
            "propagation-loss-model": "friis",
            "wp-mobility": False,
}
nNodes = int( testPar['nodes'] )    # Number of nodes in the topology to be used for processing of mp report

def onehex2dec (letter):
    value = ord(letter)
    if value > 96:
        value -= 87
    elif value > 64:
        value -= 55
    else:
        value -= 48
    return value

def mac2node (peerMac):
    lastOctet = peerMac[-2:]
    decimal = onehex2dec(lastOctet[0])*16 + onehex2dec(lastOctet[1])
    return str(decimal-1)

# Verify for arguments that select which tests to run:
# with no argument the scripts in TEST_LIST are run
# with the first argument "combine" all the combinations of parameteres specified in each dictionary of the list param_set are run
if ( len(sys.argv) > 1 ) and ( sys.argv[1] == "combine"):
    print ("Running all combination of parameters specified...\n")
    runList = False
else:
    print ("Running scripts from the predefined List...\n")

if ( len(sys.argv) > 1):
    for arg in sys.argv:
        arg_pair = arg.split('=')
        if arg_pair[0] == "skip":
            try:
                skip = int(arg_pair[1])
                print("skipping", skip, "tests...")
                break;
            except:
                print("invalid skip value, all tests are going to be executed...")

#parsing TEST_LIST and creating the command line script and also the rows of parameters for the csv file
maxColumnSize = 0
headingsOrdered = True
parsed_test_list = []   # A list of all test scripts to be run in the cmd line
param_value_csv_list = []   # A list of lists, each list contains all [param, value] pairs.
#When heading are ordered:
param_csv_list = [] # Contains all parameter names when all tests has same parameters (Headings Ordered)
value_csv_list = [] # A list of lists, each list contains all param values for a single test
#useUDP = [] (finally Not implemented as the protocol used for each stream can be obtained from the Flow Monitor xml report)
nTests = 0
testIter = 0
if runList: #Execute specific scripts in list TEST_LIST
    nTests = len (TEST_LIST)
    for current_test in  TEST_LIST:
        testIter += 1
        parsed_test = "./waf --run " + "\"" + testFileName
        param_value_csv = []
        value_csv = []
        columnSize = 0
        parameters = current_test.split()
        for parameter in parameters:
            param_pair = parameter.split('=')
            if len (param_pair) == 2:
                param_pair[0] = param_pair[0].lstrip('-')
                if param_pair[0] in physicalPar:
                    physicalPar[param_pair[0]] = "See below"
                elif param_pair[0] in networkPar:
                    networkPar[param_pair[0]] = "See below"
                elif param_pair[0] in testPar:
                    testPar[param_pair[0]] = "See below"
                if testIter == 1:
                    param_csv_list.append(param_pair[0])
                if (headingsOrdered):
                    value_csv.append(param_pair[1])
                    if (param_pair[0] not in param_csv_list):
                        headingsOrdered = False
                #if param_pair[0] == "protocol":
                #    useUDP += [True] if param_pair[1] == "udp" else [False]
                parsed_test += " --" + param_pair[0] + "=" + param_pair[1]
                param_value_csv += [ param_pair[0], param_pair[1] ]
                columnSize += 2
        parsed_test += "\""
        #Used when each test has different quantity of parameters, to adjust the column count according to the longer list of parameters
        if columnSize > maxColumnSize:
            maxColumnSize = columnSize
        parsed_test_list.append (parsed_test)
        param_value_csv_list.append (param_value_csv)
        if (headingsOrdered):
            value_csv_list.append(value_csv)
else:
    for dict in param_set:
        param_list = list (dict.keys())
        value_csv = []
        for value1 in dict[ param_list[0] ]:
            value_csv.append(value1)
            for value2 in dict[ param_list[1] ]:
                value_csv.append(value2)
                for value3 in dict[ param_list[2] ]:
                    value_csv.append(value3)
                    for value4 in dict[ param_list[3] ]:
                        value_csv.append(value4)
                        for value5 in dict[ param_list[4] ]:
                            value_csv.append(value5)
                            for value6 in dict[ param_list[5] ]:
                                value_csv.append(value6)
                                #for value7 in dict[ param_list[6] ]:
                                    #value_csv.append(value7)
                                value_csv_list.append(value_csv)
                                    #value_csv = value_csv [:-1]
                                value_csv = value_csv [:-1]
                            value_csv = value_csv [:-1]
                        value_csv = value_csv [:-1]
                    value_csv = value_csv [:-1]
                value_csv = value_csv [:-1]
            value_csv = value_csv [:-1]

    for param in param_list:
        if param in physicalPar:
            physicalPar[param] = "See below"
        elif param in networkPar:
            networkPar[param] = "See below"
        elif param in testPar:
            testPar[param] = "See below"
    param_csv_list = param_list

    for value_csv in value_csv_list:
        parsed_test = "./waf --run " + "\"" + testFileName
        i = 0
        for param in param_csv_list:
            parsed_test += " --" + param + "=" + value_csv[i]
            i += 1
        parsed_test += "\""
        parsed_test_list.append(parsed_test)
    nTests = len (parsed_test_list)

# headingsOrdered is True, we can just print the parameters row once and reduce columns in csv file by half
if (headingsOrdered):
    maxColumnSize = len (param_csv_list)

offsetRow = [] #Creates a column offset before the headings identifying flows
for i in range(maxColumnSize):
    offsetRow.append("")
if skip == 0:
    #Printing list of Physical, Network and Test Parameters to csv file
    lenP = len (physicalPar)
    lenN = len (networkPar)
    lenT = len (testPar)

    keyPhy = list(physicalPar.keys())
    keyNet = list(networkPar.keys())
    keyTes = list(testPar.keys())

    valPhy = list(physicalPar.values())
    valNet = list(networkPar.values())
    valTes = list(testPar.values())

    l = max ([lenP, lenN, lenT])

    with open(dataReportFilename, 'a', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        row =["Physical Layer Parameters", "", "PeerLink & HWMP Parameters", "", "Test Parameters"]
        filewriter.writerow(row)
        for i in range (l):
            row = []
            if i < lenP:
                row.append(keyPhy[i])
                row.append(valPhy[i])
            else:
                row.append("")
                row.append("")
            if i < lenN:
                row.append(keyNet[i])
                row.append(valNet[i])
            else:
                row.append("")
                row.append("")
            if i < lenT:
                row.append(keyTes[i])
                row.append(valTes[i])
            else:
                row.append("")
                row.append("")
            filewriter.writerow (row)
        filewriter.writerow ([" "])

'THE SCRIPT EXECUTION STARTS HERE'
#Run parsed scripts and update csv file
testIter = 0

for script in parsed_test_list:
    testIter += 1
    # If this is a continuted execution of a previous stopped list of tests, skip tests completed
    if testIter <= skip:
        continue
    # Build a filename for ascii report file and net-mp csv report file:
    testTxt = "{0:03d}".format(test_iter_offset + test_iter_increment*(testIter-1) +1)
    #testTxtAscii = "meshtest-" + testTxt + ".tr"

    #Specify the ascii report filename as an argument to the test:
    #script = script[:-1] + " --ascii-file=" + testTxtAscii + "\""

    print ("Running script", str(testIter), "of", str(nTests) + ":\n" + script)
    result = os.system (script)
    with open(dataReportFilename, 'a', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if result == 0:
            tree = ET.parse(flowMonReportFile)
            root = tree.getroot()

            #Determining flows that are received at destinationIP
            flowIds = []
            flowProtocols = []
            for flow in root.findall('Ipv4FlowClassifier/Flow'):
                if flow.attrib['destinationAddress'] == destinationIP:
                    flowIds.append(flow.attrib['flowId'])
                    flowProtocols.append(flow.attrib['protocol'])

            #Printing stats title row
            if testIter == 1:
                if (headingsOrdered):
                    row = param_csv_list
                else:
                    row = offsetRow
                for flow in flowIds:
                    row.append("TP_Flow_" + flow)
                row.append("TotRxPackets")
                row.append("TotRxDataBytes")
                for flow in flowIds:
                    # Cumulative delay
                    row.append("CD_Flow_" + flow)
                row.append("TotDelaySum_us")
                row.append("AvgDelay_us")
                if logRouteChanges:
                    row.append("RouteChanges")
                filewriter.writerow(row)

            #Obtaining statistics from flows identified
            statRow = []
            statRowDelay = []
            flowIter = 0
            totalRxDataBytes = 0
            for flow in root.findall('FlowStats/Flow'):
                if flow.attrib['flowId'] in flowIds:
                    rxPackets = int(flow.attrib['rxPackets'])
            # Need to change this, flows are numbered in the order the application starts (headings), but the stats are ordered in ascending flow number (content)
                    statRow.append(rxPackets)
                    delaySumTxt = flow.attrib['delaySum']
                    delaySum = float(delaySumTxt[:-2])/1000 # Store the value in microseconds
                    statRowDelay.append(delaySum)
                    overhead = 28 if flowProtocols[flowIter] == "17" else 52 if flowProtocols[flowIter] == "6" else 0
                    totalRxDataBytes += int(flow.attrib['rxBytes']) - overhead*rxPackets
            totalRxPackets = sum(statRow)
            statRow.append(totalRxPackets)
            statRow.append(totalRxDataBytes)
            statRow.extend(statRowDelay)
            statRow.append(sum(statRowDelay))
            if totalRxPackets != 0:
                statRow.append(sum(statRowDelay)/totalRxPackets)
            else:
                statRow.append("")
            if logRouteChanges:
                rChangeHstgFilename = rChangeHstgBaseName + testTxt + '.csv'
                rChanges = genRChangeHistogram (rChangeHstgFilename, rChangesReportFilename, nNodes, destinationMAC)
                statRow.append(rChanges)
            # Join parameters and stats row
            if (headingsOrdered):
                row = value_csv_list[testIter-1] + statRow
            else:
                row = param_value_csv_list[testIter-1]
                for i in range(maxColumnSize - len(param_value_csv_list[testIter-1])):
                    row.append("")
                row.extend(statRow)
            filewriter.writerow(row)
            print("\n" + dataReportFilename + " file has been updated.")

            # Processing and summary of mp-report xml files
            mpSummaryReportFilename = mpSummaryReportBaseName + testTxt + '.csv'
            with open(mpSummaryReportFilename, 'a', newline='') as mpSummaryCsv:
                mpSummaryWriter = csv.writer(mpSummaryCsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                mpSummaryWriter.writerow(["node", "root", "TxUnicastData", "txUnicastDataBytes", "rxUnicastData", "rxUnicastDataBytes", "fwdUnicastData", "fwdUnicastDataBytes",
                                        "txUnicast", "txBroadcast", "txBytes", "droppedTtl", "totalQueued", "totalDropped", "initiatedPreq", "initiatedPrep",
                                        "initiatedPerr", "initiatedLpp", "txPreq", "txPrep", "txPerr", "txLpp", "rxPreq", "rxPrep", "rxPerr", "rxLpp", "txMgt", "txMgtBytes",
                                        "rxMgt", "rxMgtBytes", "txData", "txDataBytes", "rxData", "rxDataBytes", "txOpen", "txConfirm", "txClose", "rxOpen", "rxConfirm",
                                        "rxClose", "dropped", "brokenMgt", "txMgt", "txMgtBytes", "rxMgt", "rxMgtBytes", "beaconShift", "rootNextHop", "rootMetric", "linksOpened",
                                        "linksClosed", "linksTotal"])
                for n in range (nNodes):
                    row = []
                    row.append( str(n) )
                    mpReportFilename = mpReportBaseName + str(n) + '.xml'
                    tree = ET.parse(mpReportFilename)
                    root = tree.getroot()
                    # is root?
                    hwmp = root.findall('Hwmp')
                    isRoot = False
                    if hwmp[0].attrib['isRoot'] == "1":
                        row.append("yes")
                        isRoot = True
                    else:
                        row.append("no")
                    # General Statistics
                    for stats in root.findall('Statistics'):
                        row.append(stats.attrib['txUnicastData'])
                        row.append(stats.attrib['txUnicastDataBytes'])
                        row.append(stats.attrib['rxUnicastData'])
                        row.append(stats.attrib['rxUnicastDataBytes'])
                        row.append(stats.attrib['fwdUnicastData'])
                        row.append(stats.attrib['fwdUnicastDataBytes'])
                    # hwmp statistics
                    for hwmpStats in root.findall('Hwmp/Statistics'):
                        row.append(hwmpStats.attrib['txUnicast'])
                        row.append(hwmpStats.attrib['txBroadcast'])
                        row.append(hwmpStats.attrib['txBytes'])
                        row.append(hwmpStats.attrib['droppedTtl'])
                        row.append(hwmpStats.attrib['totalQueued'])
                        row.append(hwmpStats.attrib['totalDropped'])
                        row.append(hwmpStats.attrib['initiatedPreq'])
                        row.append(hwmpStats.attrib['initiatedPrep'])
                        row.append(hwmpStats.attrib['initiatedPerr'])
                        row.append(hwmpStats.attrib['initiatedLpp'])
                    # hwmp protocolmac statistics
                    for hwmpMacStats in root.findall('Hwmp/HwmpProtocolMac/Statistics'):
                        row.append(hwmpMacStats.attrib['txPreq'])
                        row.append(hwmpMacStats.attrib['txPrep'])
                        row.append(hwmpMacStats.attrib['txPerr'])
                        row.append(hwmpMacStats.attrib['txLpp'])
                        row.append(hwmpMacStats.attrib['rxPreq'])
                        row.append(hwmpMacStats.attrib['rxPrep'])
                        row.append(hwmpMacStats.attrib['rxPerr'])
                        row.append(hwmpMacStats.attrib['rxLpp'])
                        row.append(hwmpMacStats.attrib['txMgt'])
                        row.append(hwmpMacStats.attrib['txMgtBytes'])
                        row.append(hwmpMacStats.attrib['rxMgt'])
                        row.append(hwmpMacStats.attrib['rxMgtBytes'])
                        row.append(hwmpMacStats.attrib['txData'])
                        row.append(hwmpMacStats.attrib['txDataBytes'])
                        row.append(hwmpMacStats.attrib['rxData'])
                        row.append(hwmpMacStats.attrib['rxDataBytes'])
                    # peer management protocolmac statistics
                    for peerProtocolMacStats in root.findall('PeerManagementProtocol/PeerManagementProtocolMac/Statistics'):
                        row.append(peerProtocolMacStats.attrib['txOpen'])
                        row.append(peerProtocolMacStats.attrib['txConfirm'])
                        row.append(peerProtocolMacStats.attrib['txClose'])
                        row.append(peerProtocolMacStats.attrib['rxOpen'])
                        row.append(peerProtocolMacStats.attrib['rxConfirm'])
                        row.append(peerProtocolMacStats.attrib['rxClose'])
                        row.append(peerProtocolMacStats.attrib['dropped'])
                        row.append(peerProtocolMacStats.attrib['brokenMgt'])
                        row.append(peerProtocolMacStats.attrib['txMgt'])
                        row.append(peerProtocolMacStats.attrib['txMgtBytes'])
                        row.append(peerProtocolMacStats.attrib['rxMgt'])
                        row.append(peerProtocolMacStats.attrib['rxMgtBytes'])
                        row.append(peerProtocolMacStats.attrib['beaconShift'])
                    # Route to Root Node
                        pRoute = root.find('Hwmp/RoutingTable/ProactiveRoute')
                        row.append(pRoute.get('retransmitter') if not isRoot else "N/A")
                        row.append(pRoute.get('metric') if not isRoot else "0")
                    # peer management protocol statistics
                    for peerProtocolStats in root.findall('PeerManagementProtocol/Statistics'):
                        row.append(peerProtocolStats.attrib['linksOpened'])
                        row.append(peerProtocolStats.attrib['linksClosed'])
                        row.append(peerProtocolStats.attrib['linksTotal'])
                    # peer links
                    for peerLink in root.findall('PeerManagementProtocol/PeerLink'):
                        peerMac = peerLink.attrib['peerInterfaceAddress']
                        wifiMode = peerLink.attrib['wifiMode']
                        metric = peerLink.attrib['metric']
                        row.append(mac2node (peerMac) + '=' + wifiMode + ":" + metric)
                    # add node report information to csv file
                    mpSummaryWriter.writerow(row)
                print(mpSummaryReportFilename + " file has been created.\n")
        else:
            if (headingsOrdered):
                row = value_csv_list[testIter-1]
            else:
                row = param_value_csv_list[testIter-1]
            row.append("This test generated an error.")
            filewriter.writerow(row)
            print("While running the last script, an error occurred.\n")
