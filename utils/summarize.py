
import xml.etree.ElementTree as ET
import csv

mpReportBaseName = 'mp-report-'
mpSummaryReportBaseName = 'net-mp-report-'

testTxt = "single"
nNodes = 60

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

# Processing and summary of mp-report xml files
mpSummaryReportFilename = mpSummaryReportBaseName + testTxt + '.csv'
with open(mpSummaryReportFilename, 'a', newline='') as mpSummaryCsv:
    mpSummaryWriter = csv.writer(mpSummaryCsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    mpSummaryWriter.writerow(["node", "root", "txUnicast", "txBroadcast", "txBytes", "droppedTtl", "totalQueued", "totalDropped", "initiatedPreq", "initiatedPrep",
                            "initiatedPerr", "initiatedLpp", "txPreq", "txPrep", "txPerr", "txLpp", "rxPreq", "rxPrep", "rxPerr", "rxLpp", "txMgt", "txMgtBytes",
                            "rxMgt", "rxMgtBytes", "txData", "txDataBytes", "rxData", "rxDataBytes", "txOpen", "txConfirm", "txClose", "rxOpen", "rxConfirm",
                            "rxClose", "dropped", "brokenMgt", "txMgt", "txMgtBytes", "rxMgt", "rxMgtBytes", "beaconShift", "linksOpened", "linksClosed",
                            "linksTotal", "links"])
    for n in range (nNodes):
        row = []
        row.append( str(n) )
        mpReportFilename = mpReportBaseName + str(n) + '.xml'
        tree = ET.parse(mpReportFilename)
        root = tree.getroot()
        # is root?
        hwmp = root.findall('Hwmp')
        if hwmp[0].attrib['isRoot'] == "1":
            row.append("yes")
        else:
            row.append("no")
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
        # peer management protocol statistics
        for peerProtocolStats in root.findall('PeerManagementProtocol/Statistics'):
            row.append(peerProtocolStats.attrib['linksOpened'])
            row.append(peerProtocolStats.attrib['linksClosed'])
            row.append(peerProtocolStats.attrib['linksTotal'])
        # peer links
        for peerLink in root.findall('PeerManagementProtocol/PeerLink'):
            peerMac = peerLink.attrib['peerInterfaceAddress']
            wifiMode = peerLink.attrib['wifiMode']
            row.append(mac2node (peerMac) + '=' + wifiMode)
        # add node report information to csv file
        mpSummaryWriter.writerow(row)
    print(mpSummaryReportFilename + " file has been created.\n")
