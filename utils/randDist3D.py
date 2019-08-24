# DESCRIPTION: Random 3D Coordinates generator
# AUTHOR: Oscar Bautista <obaut004@fiu.edu>

from random import *
from math import *

# Min Between nodes in the distribution
MIN_DISTANCE = 100	#90
# Max Distance to closest node, this guarantees that the new node is not going to be too far from existing nodes
MAX_DISTANCE = 250	#210
# Number on Nodes in each distribution
nodes = 60  #20
# Cube that limits the location of random coordinate points
xDim = 2400	#1600  	#550	#400		(for 60/40/40/20 nodes)
yDim = 1200	#900  	#350	#250
zDim = 120	#110	#105	#100
zMin = 30	#20	#20	#20
#Number of distributions to create
nDistributions = 60
#Name of file to store the random Distributions
filename = "n_eq_60_3d.h"

file = open (filename, "w+")
file.write("using namespace std;\n")
file.write("//Constraints: min distance %.1fm, max distance %.1fm\n" % (MIN_DISTANCE, MAX_DISTANCE) )
file.write("struct coordinates %s[%d][%d] = {\n" % (filename[:-2], nDistributions, nodes) )

for k in range (nDistributions):
    print("Finding random Distribution", str(k+1))
    file.write("{ //#%d\n" % (k) )
    nodeLoc = []
    zVector = []    #Used to store all z coordinates for later on selecting the highest location
    i = 0
    while i < nodes:
        newNodeDistances = []
        x= randint(1, xDim*10+1)/10
        y= randint(1, yDim*10+1)/10
        # Minimum height is 20m. Friis propagation loss model is Z dependent, therefore an additional constraint is set to avoid higher attenuations
        z= randint(zMin*10, zDim*10+1)/10
        if i == 0:
            nodeLoc.append([x, y, z])
            zVector.append(z)
            i+= 1
            continue
        tooClose= False
        for j in range(i):
            x1=nodeLoc[j][0]
            y1=nodeLoc[j][1]
            z1=nodeLoc[j][2]
            distance= sqrt((x1-x)**2+(y1-y)**2+(z1-z)**2)
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
                zVector.append(z)
                i+= 1
    # Obtaining the index of the highest point or node
    mIndex = zVector.index(max(zVector))

    # Sorting the 3D points to have the highest point at index 0
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
