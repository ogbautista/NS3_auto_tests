'''
* Copyright (c) 2019 - 2020 Oscar Bautista
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License version 2 as published
* by the Free Software Foundation.
*
* DESCRIPTION:
* Converts the Course Change information obtained after an NS3 simulation to Bonnmotion format
*
* AUTHOR: Oscar Bautista <obaut004@fiu.edu>
'''
import sys
from my_utils import fRead
from my_utils.ns3Time import Ns3Time
from my_utils.ns3Vector import Ns3Vector

if len(sys.argv) < 3:
    print ("\nUsage:\npython course2bm.py 'waypointsfile.csv' 'bonnmotionfile.movements' [maxtime=...]\n")
    sys.exit(1)

sourceFile = sys.argv[1]
bmScenarioFile = sys.argv[2]
scn3D = False

# This dictionary stores the movement information for each node as a list element
bmMovements = {}

waypoints = fRead.get_csvdict(sourceFile)
for waypoint in waypoints:
    try:
        node = int(waypoint['Node'])
        time = Ns3Time(waypoint['Time']).getSeconds()
        position = Ns3Vector(waypoint['Position'])
    except KeyError as e:
        print("KeyError: {}".format(e))
        sys.exit(1)
    # If any Z coordinate is different than 0, then it is considered a 3D constellation
    if not scn3D and position.z != 0:
        scn3D = True

    if node in bmMovements:
        bmMovements[node].extend([time, position.x, position.y, position.z])
    else:
        # First Waypoint stored as initial Waypoint
        if time > 0:
            bmMovements[node] = [0.0, position.x, position.y, position.z]
        try:
            bmMovements[node].extend([time, position.x, position.y, position.z])
        except KeyError:
            bmMovements[node] = [time, position.x, position.y, position.z]

# Creates output file and stores the data
try:
    with open(bmScenarioFile, 'w') as movementsfile:
        if scn3D:
            movementsfile.write("#3D\n")
        for node, data in sorted(bmMovements.items()):
            line = ""
            for i in range(0, len(data), 4):
                line += f"{data[i]} {data[i+1]} {data[i+2]} "
                if scn3D:
                    line += f"{data[i+3]} "
            line = line.strip()+'\n'
            movementsfile.write(line)
    print ("Successfully created {}\n".format(bmScenarioFile))
except:
    print("Error while writing to file {}: {}, {}".format(bmScenarioFile, sys.exc_info()[0], sys.exc_info()[1]))
    sys.exit(1)
