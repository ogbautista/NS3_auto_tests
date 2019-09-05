'''
* Copyright (c) 2019 - 2020 Oscar Bautista
*
* This program is free software; you can redistribute it and/or modify it
* under the terms of the GNU General Public License version 2 as published
* by the Free Software Foundation.
*
* AUTHOR: Oscar Bautista <obaut004@fiu.edu>
'''

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

# Converts a MAC address to decimal then to node number (assumes MAC and node number are ordered)
def macAddr2node (peerMac):
    last2octets = peerMac[-5:-3] + peerMac[-2:]
    decimal = int (last2octets, 16)
    return str(decimal-1)
