# DESCRIPTION: Random 2D Coordinates generator
# AUTHOR: Oscar Bautista <obaut004@fiu.edu>

from random import *
from math import *

# Min Between nodes in the distribution
MIN_DISTANCE = 130
# Max Distance to closest node, this guarantees that the new node is not going to be too far from existing nodes
MAX_DISTANCE = 245
# Number on Nodes in each distribution
nodes = 60
# Cube that limits the location of random coordinate points
xDim = 2400
yDim = 1200
zDim = 17   #All points located at this height

#Number of distributions to create
nDistributions = 60
#Name of file to store the random Distributions
filename = "n_eq_60_2d.h"

file = open (filename, "w+")
file.write("using namespace std;\n")
file.write("//Constraints: min distance %.1fm, max distance %.1fm\n" % (MIN_DISTANCE, MAX_DISTANCE) )
file.write("struct coordinates %s[%d][%d] = {\n" % (filename[:-2], nDistributions, nodes) )

for k in range (nDistributions):
    print("Finding random Distribution", str(k+1))
    file.write("{ //#%d\n" % (k) )
    nodeLoc = []
    i = 0
    xL = None
    xH = None
    yL = None
    yH = None
    while i < nodes:
        newNodeDistances = []
        x= randint(1, xDim*10+1)/10
        y= randint(1, yDim*10+1)/10
        z= zDim
        if i == 0:
            nodeLoc.append([x, y, z])
            xL = x
            xH = x
            yL = y
            yH = y
            i+= 1
            continue
        tooClose= False
        for j in range(i):
            x1=nodeLoc[j][0]
            y1=nodeLoc[j][1]
            distance= sqrt((x1-x)**2+(y1-y)**2)
            if distance < MIN_DISTANCE:
                tooClose= True
                break
            else:
                newNodeDistances.append(distance)
        if not tooClose:
            if (min(newNodeDistances) > MAX_DISTANCE):
                continue
            else:
                nodeLoc.append([x, y, z])
                xL = x if x < xL else xL
                xH = x if x > xH else xH
                yL = y if y < yL else yL
                yH = y if y > yH else yH
                i+= 1

    # Obtaining the index of the 2D location closest to the center
    xMedian = (xL+xH)/2;
    yMedian = (yL+yH)/2;
    mIndex = None
    minDistance = None
    for i in range(nodes):
        distance = sqrt((xMedian - nodeLoc[i][0])**2 + (yMedian - nodeLoc[i][1])**2)
        if minDistance is not None:
            if distance < minDistance:
                minDistance = distance
                mIndex = i
        else:
            minDistance = distance
            mIndex = i

    # Sorting the 2D points to have the more centered point at index 0
    nodeLoc.insert(0,nodeLoc.pop(mIndex))

    # Adds new distribution to file
    for i in range(nodes):
        file.write("\t{ %.1f , %.1f , %.1f }" % (nodeLoc[i][0], nodeLoc[i][1], nodeLoc[i][2]) )
        if i != (nodes - 1):
            file.write(",\n")
        else:
            file.write("\n")
    if k != (nDistributions - 1):
        file.write("},\n")
    else:
        file.write("}\n")
file.write("};")
file.close()
print(nDistributions, "distributions stored at file", filename)
