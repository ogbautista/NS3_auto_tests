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
    print ("\nUsage:\npython3 ns3toBm.py 'waypointsfile.csv' 'bonnmotionfile.movements' [stime=...]\n")
    sys.exit(1)

sourceFile = sys.argv[1]
bmScenarioFile = sys.argv[2]
scn3D = False
simtime = None
# Simulation time stime is specified to indicate that the scenario duration extends beyond the last waypoint time
if len(sys.argv) >= 4:
    argpair = sys.argv[3].split('=')
    if len(argpair) == 2 and argpair[0] == "stime":
        try:
            simtime = float(argpair[1])
        except ValueError as e:
            print(e, "...ignored")
    else:
        print("Invalid argument: '{}' ...ignored".format(argpair[0]))

# This dictionary stores the movement information for each node as a list element
bmMovements = {}
# Read and process data from the source file
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
        bmMovements[node] = [0.0, position.x, position.y, position.z]
        if time > 0:
            bmMovements[node].extend([time, position.x, position.y, position.z])

# Creates output file and stores the data
try:
    with open(bmScenarioFile, 'w') as movementsfile:
        if scn3D:
            movementsfile.write("#3D\n")
        for node, data in sorted(bmMovements.items()):
            # insert one more waypoint if simulation time beyond last waypoint is specifie as argument
            if simtime is not None and data[-4] < simtime:
                lastwp = data[-3:]
                data.append(simtime)
                data.extend(lastwp)
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
