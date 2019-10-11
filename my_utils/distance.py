import sys
import re
from math import *

def getkey(item):
    return item[1]

def printNodes(mydistances):
    lines = len (mydistances) if len (mydistances) < 20 else 20
    print("Printing distance to 20 closest nodes...\n")
    print("Node:\tDistance:")
    print("----\t--------")
    for i in range(lines):
        nodeStr = str (mydistances[i][0])
        nodeStr = " "*(4-len(nodeStr)) + nodeStr
        distanceStr = str (mydistances[i][1])
        distanceStr = " "*(4-len(distanceStr.split(".")[0])) + distanceStr
        print (nodeStr + "\t" + distanceStr)
    print("\n" + str(lines) + " distances displayed.\n")

filename = None
if ( len(sys.argv) > 1 ):
    filename = sys.argv[1]

while True:
    if filename is None:
        filename = input ("Coordinates file: ")
        if filename == "":
            quit()
    try:
        f = open (filename, "r")
        print ("File", filename, "opened")
        break
    except:
        print ("There was an error opening the specified file\n")
        filename = None

content = f.readlines()
f.close()

topoIdNum = None
nodeNum = None
executeMain = True
numVal = re.compile(r"\d+[.\d]*")

while executeMain:
    nNodes = 0
    X = []
    Y = []
    Z = []
    # While loop executed until a valid topology number is given
    while True:
        topoID = input ("Topology number to analyze" + ( " [" + (str (topoIdNum) + "]: " )if topoIdNum is not None else ": " ) )
        if (topoIdNum is None) and topoID == "":
            executeMain = False
            print("exiting now...\n")
            break
        try:
            if topoID != "":
                topoIdNum = int(topoID)
            break
        except:
            print ('', end = '')
    # Ask for a node number and then search the file content for it, gets and process the content
    while executeMain:
        node = input ("Node number: ")
        if node == "":
            executeMain = False
            print("exiting now...\n")
            break
        try:
            nodeNum = int(node)
            found = False
            topoIndex = re.compile("//#" + str(topoIdNum))

            for line in content:
                if not found:
                    indexMatch = topoIndex.findall(line)
                    if len (indexMatch) > 0:
                        print("Topology found, reading coordinates...", end="")
                        found = True
                else:
                    coordinates = numVal.findall(line)
                    if len (coordinates) == 0:
                        # There is no more coordinates for this topology number
                        print("done")
                        break
                    else:
                        X.append(float (coordinates[0]))
                        Y.append(float (coordinates[1]))
                        Z.append(float (coordinates[2]))
                        nNodes += 1

            # If the topology is found, then the distances from the specified node to every other node is calculated:
            if found:
                if nodeNum > (nNodes - 1):
                    print("This topology contains just", str(nNodes), "nodes")
                    break
                distancesV = []
                #print(X[nodeNum], Y[nodeNum], Z[nodeNum])
                for i in range(nNodes):
                    if i == nodeNum:
                        continue
                    #print(X[i], Y[i], Z[i])
                    distance = int (sqrt ( (X[i]-X[nodeNum])**2 + (Y[i]-Y[nodeNum])**2 + (Z[i]-Z[nodeNum])**2 ) * 100)/100
                    distancesV.append( (i, distance) )
                printNodes(sorted (distancesV, key=getkey))
                break
            else:
                print ("Topology number NOT found!\n")
                break

        except:
            print ('', end = '')
