'''
* Copyright (c) 2019 - 2020 Oscar Bautista
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License version 2 as published
* by the Free Software Foundation.
*
* DESCRIPTION:
* Resource functions to read content from different file types, used by NS-3 simulation reports
* post-processing utilities.
*
* AUTHOR: Oscar Bautista <obaut004@fiu.edu>
'''

import sys, re, csv

'''
Reads an XML File, whose name is passed as an argument from the command line at position 'index'. If no filename is given, it is prompted for input from the user.
RETURNS the filename and the xml root.'''
def tree_xmlfile_prompt (index):
    filename = None
    if ( len(sys.argv) > index ):
        filename = sys.argv[index]
    while True:
        if filename is None:
            filename = input ("XML File: ")
        if filename == "":
            print("exiting now...\n")
            quit()
        try:
            print ("Opening and parsing file", filename + "...", end = "")
            tree = ET.parse(filename)
            print ("done")
            break
        except:
            print ("there was an error opening/parsing the specified file\n")
            filename = None
    return filename, tree.getroot()

'''
Reads a file with specific format containing 3d coordinates, whose name is passed as an argument from the command line at position 'index' or as an argument to the function.
If no filename is given, it is prompted for input from the user.
RETURNS the topology number and 3 lists corresponding to the values of each coordinate's dimension.'''
def get_coordinates_prompt (index = None, filenameRef = [None], topoId = None):
    filename = filenameRef[0]
    if ( index is not None and len(sys.argv) > index ):
        filename = sys.argv[index]
    while True:
        if filename is None:
            filename = input ("Coordinates file: ")
        if filename == "":
            print("exiting now...\n")
            quit()
        try:
            print ("Opening coordinates file", filename + "...", end = "")
            f = open (filename, "r")
            print ("done")
            filenameRef[0] = filename
            break
        except:
            print ("there was an error opening the specified file\n")
            filename = None
    content = f.readlines()
    f.close()
    # Request Topology Number and read coordinates
    numVal = re.compile(r"\d+[.\d]*")
    X = []
    Y = []
    Z = []
    if ( index is not None and len (sys.argv) > index+1 ):
        s_topoId = sys.argv[index+1]
    elif topoId is None:
        s_topoId = None
    else:
        s_topoId = str (topoId)
    found = False
    while not found:
        if s_topoId is None:
            s_topoId = input ("Topology number to graph: ")
        if s_topoId == "":
            print("exiting now...\n")
            quit()
        try:
            topoId = int(s_topoId)
        except:
            print ("Topology number...expects an integer")
            s_topoId = None
            continue
        topoIndex = re.compile("//#" + s_topoId)
        for line in content:
            if not found:
                indexMatch = topoIndex.findall(line)
                if len (indexMatch) > 0:
                    print("Topology #{} found, reading coordinates...".format(topoId), end = "")
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
        if not found:
            print ("Topology number NOT found!")
            s_topoId = None
    return topoId, X, Y, Z

'''
Reads a CSV file with specific format containing summary report for a specific network simulation. The filename is passed as an argument from the command line
at position 'index' or as an argument to the function. If no filename is given, it is prompted for input from the user.
RETURNS a generator object which produces Node Records as an OrderedDict.'''
def get_csvdict_prompt (index = None, filenameRef = [None]):
    filename = filenameRef[0]
    if ( index is not None and len(sys.argv) > index ):
        filename = sys.argv[index]
    while True:
        if filename is None:
            filename = input ("Network MeshPoint Report File: ")
            if filename == "":
                print("exiting now...\n")
                quit()
        try:
            print ("Opening and reading file", filename + "...", end = "")
            with open (filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile, restkey = 'links')
                filenameRef[0] = filename
                for row in reader:
                    yield row
            break
        except:
            print ("there was an error during the process of getting information from the specified file\n")
            filename = None
    print ("done")
