import xml.etree.ElementTree as ET
import csv

tree = ET.parse('MyMeshPerformance.xml')
root = tree.getroot()

row =[]
for flow in root.findall('FlowStats/Flow'):
    row.append(int(flow.attrib['rxPackets']))
    #print (flow.attrib['rxPackets'])
row.append(sum(row))

header =[]
for i in range(len(row)):
    header.append('flow ' + str(i+1))
header.append('total')

with open('rxPacketsSummary.csv', 'a', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #filewriter.writerow(header)
    filewriter.writerow(row)
