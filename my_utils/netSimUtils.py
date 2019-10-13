'''
* Copyright (c) 2019 - 2020 Oscar Bautista
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License version 2 as published
* by the Free Software Foundation.
*
* AUTHOR: Oscar Bautista <obaut004@fiu.edu>
'''
import math
# Covenverts a single hexadecimal character to decimal
# unused, python has already a function for that using int (hex, base)
def onehex2dec (letter):
    value = ord(letter)
    if value > 96:
        value -= 87
    elif value > 64:
        value -= 55
    else:
        value -= 48
    return value

# Converts a MAC address string to decimal then to node number (assumes MAC and node number are ordered)
def macAddr2node (peerMac):
    last2octets = peerMac[-5:-3] + peerMac[-2:]
    decimal = int (last2octets, 16)
    return str(decimal-1)

# Calculates the margin of a matplotlib 2D figure based on the relation between x and y axes dimension
# This nargins are optimized for a specific general figure dimension
def getPlotMargins (xyRelation):
    top = 0.917+0.075*math.log10(xyRelation)
    bottom = 0.098-0.092*math.log10(xyRelation)
    if xyRelation < 1:
        left = 0.04+0.08*xyRelation
        right = 0.98-0.04*xyRelation
    elif xyRelation < 1.25:
        left = 0.12*xyRelation
        right = 0.98-0.04*xyRelation
    else:
        left = 0.1+0.04*xyRelation
        right = 0.9475-0.014*xyRelation
    margins = dict(left=left, right=right, top=top, bottom=bottom)
    return margins

# Calculates and optimized xy relation given a matplotlib fig x and y dimensions, also calculates a suggested figure size
def calculateFigDimensions(xLim, yLim):
    xyRelation = yLim/xLim
    # a little tweaking reduces large differences:
    xyRelation = xyRelation/(1.03*2.2**math.log10(xyRelation))
    # When using plt.figaspect() a xyRelation = 1 produces a smaller figure compared to rectangular figure aspects
    # a little tweaking tries to reduce this effect
    sizeMultiplier = 1.35-abs(1.05*math.log10(xyRelation/1.07))
    return xyRelation, sizeMultiplier

# z lim in a matplotlib 3D plot is calculated based on the x and y axes limits, trying to make it less disproportionated
def calculateZlim (xlim, ylim, zlim):
    rel = min(xlim, ylim, key=abs)/abs(zlim)
    if rel > 2:
        multiplier = math.log10(rel)/math.log10(2)
        newZlim = round(zlim * multiplier / 10)*10
        return newZlim
    else:
        return zlim
