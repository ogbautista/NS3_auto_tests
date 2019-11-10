from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys
import re
import time

filename = None
if ( len(sys.argv) > 1 ):
    filename = sys.argv[1]

while True:
    if filename is None:
        filename = input ("Coordinates file: ")
        if filename == "":
            quit()
    try:
        print ("Opening file", filename + "...", end='')
        f = open (filename, "r")
        print ("done")
        break
    except:
        print ("error opening the specified file\n")
        filename = None

content = f.readlines()
f.close()

#print(content)
topoIdNum = None
executeMain = True
numVal = re.compile(r"\d+[.\d]*")

while executeMain:
    topoID = input ("Topology number to graph: ")
    X = []
    Y = []
    Z = []
    nNodes = 0
    try:
        if topoID == "":
            executeMain = False
            print("exiting now...\n")
        topoIdNum = int(topoID)

        found = False
        topoIndex = re.compile("//#" + str(topoIdNum))

        for line in content:
            if not found:
                indexMatch = topoIndex.findall(line)
                if len (indexMatch) > 0:
                    print("Topology found, reading coordinates...", end='')
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
        # If the topology is found, it is graphed:
        if found:
            print("Building figure...")
            # Aspect ratio width vs height: 0.3, figure scaling: 0.5
            fig = plt.figure(figsize = plt.figaspect(0.4)*0.7)
            fig.canvas.set_window_title('Drone Deployment')
            #ax = fig.add_subplot (111, projection='3d')
            ax = fig.gca(projection='3d')
            ax.view_init (elev= 30, azim= -70)
            plt.subplots_adjust(left= -0.08, bottom= 0.04, right= 1.03, top= 0.9)
            ax.title.set_text( str(nNodes) + "-node topology #" + str(topoIdNum) )
            ax.scatter(X[0], Y[0], Z[0], s=15, c='r', marker='o')
            ax.scatter(X[1:], Y[1:], Z[1:], s=15, c='b', marker='o')
            ax.set_xlabel('x axis')
            ax.set_ylabel('y axis')
            ax.set_zlabel('z axis')
            #ax.plot([X[0], X[1]], [Y[0], Y[1]], [Z[0], Z[1]])
            for i in range (len (X)):
                 ax.text(X[i], Y[i], Z[i], '%s' % (str(i)), size=8, zorder=1, color='k')
            # plt.axes().set_aspect('equal', 'datalim') # This converts the figure to 2D
            plt.show()
            print("Figure for topology", str(topoIdNum), "closed.")
        else:
            print ("Topology number NOT found!\n")
    except:
        print('', end = '')
