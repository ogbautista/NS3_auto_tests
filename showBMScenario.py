'''
* Copyright (c) 2019 - 2020 Oscar Bautista
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License version 2 as published
* by the Free Software Foundation.
*
* DESCRIPTION:
* Generates an matplotlib animation of the nodes in a mobility scenario created using BonnMotion
*
* AUTHOR: Oscar Bautista <obaut004@fiu.edu>
'''

from utils import fRead
import math
#import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print("")
print("\t****************************************************************")
print("\t*              BonnMotion Scenario Visualization               *")
print("\t****************************************************************\n")

scnName = input("Scenario name (without '.movements'): ")
interval = 0.5
# Calculates the velocity vector of a node given an initial and final locations and corresponding times
def calculateNodeVelocity(nodeTimes, nodeLocations, nVelocity):
    nVelocity.clear()
    if len(nodeTimes) == 1:
        nVelocity.extend([0,0])
        if scn3D:
            nVelocity.append(0)
    else:
        timeSpan = nodeTimes[1] - nodeTimes[0]
        xVel = (nodeLocations[1][0] - nodeLocations[0][0])/timeSpan
        nVelocity.append(xVel)
        yVel = (nodeLocations[1][1] - nodeLocations[0][1])/timeSpan
        nVelocity.append(yVel)
        if scn3D:
            zVel = (nodeLocations[1][2] - nodeLocations[0][2])/timeSpan
            nVelocity.append (zVel)
# Read the BonnMotion scenario file and returns times and locations lists
times, locations = fRead.read_bmScenario(scnName + ".movements")

if len(times) == 0:
    quit()
scn3D = (len(locations[0][0]) == 3)

def locationGenerator(times, locations, interval):
    currentTime = times[0][0] # Assumed to be the same for all nodes
    endTime = times[0][-1] # Assumed to be the same for all nodes
    velocities = []
    # Calculation of initial Velocity of each node
    for nodeTimes, nodeLocations in zip (times, locations):
        currentNodeVelocity = []
        calculateNodeVelocity (nodeTimes, nodeLocations, currentNodeVelocity)
        velocities.append(currentNodeVelocity)
    # Generation of X, Y, Z Vectors containing location coordinates of all nodes at the current frame
    for f in range(0, math.ceil(endTime/interval)+1):
        X = []
        Y = []
        if scn3D:
            Z = []
        for nodeTimes, nodeLocations, nVelocity in zip(times, locations, velocities):
            if len(nodeTimes) == 1:
                X.append(nodeLocations[0][0])
                Y.append(nodeLocations[0][1])
                if scn3D:
                    Z.append(nodeLocations[0][2])
                continue
            if currentTime > nodeTimes[1]:
                # Use del to modify the same list that will update the times and locations variables
                del nodeTimes[0]
                del nodeLocations[0]
                calculateNodeVelocity(nodeTimes, nodeLocations, nVelocity)
            t = currentTime - nodeTimes[0]
            x = nodeLocations[0][0] + nVelocity[0]*t
            y = nodeLocations[0][1] + nVelocity[1]*t
            X.append(x)
            Y.append(y)
            if scn3D:
                z = nodeLocations[0][2] + nVelocity[2]*t
                Z.append(z)
        if scn3D:
            yield X, Y, Z
        else:
            yield X, Y
        currentTime += interval

locationFrame = locationGenerator(times, locations, interval)

# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=1800)

gifwriter = animation.ImageMagickWriter ()
#print("The delay is:", gifwriter.delay)
#gifwriter.delay = 500
#print("New delay is:", gifwriter.delay)

# Preparation of Figure
fig = plt.figure(figsize=(10,6))
fig.canvas.set_window_title("Mesh Network Animation Example")
plt.xlim(0, 3600)
plt.ylim(0, 1200)
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title("BonnMotion's Reference Point Group Mobility", fontsize = 14)
ax = fig.gca()

# Sample location to initialize global variable currentSet
currentSet = ax.scatter(0,0)
# print("Extra Parameters")
# print(plt.rcParams)

# Function to plot every frame in the figure
def update(coordinates):
    global counter, currentSet
    currentSet.remove()
    currentSet = ax.scatter(coordinates[0], coordinates[1], s= 15, c = 'b')

# The matplotlib animation function
anim = animation.FuncAnimation(fig, update, frames=locationFrame, interval=interval*100, save_count=400, repeat_delay= 1000, repeat=False)
#anim.save("MobilScn2D3.mp4")
#anim.save('MobilScn2D4.gif', writer=gifwriter, fps=20, dpi=80)
anim.save('MobilScn2D4.gif', writer='imagemagick', fps=30, dpi=75, extra_args=None)
#anim.save('MobilScn2D4.mp4', writer='ffmpeg', fps=20, dpi=80)
#ani.save('RPGM.mp4', writer=writer)
#plt.show()
