import socket
import struct
import textwrap

# Unpack ethernet frame.
def ethernetFrame ( data ):
    # Acording to the ethernet frame, takes de 6 octets of the destination MAC address.
    # the 6 octets of the source MAC address and the 2 octets of the etherType or protocol.
    destinationMAC, sourceMAC, protocol = struct.unpack ( '! 6s 6s H', data [ :14 ] )
    return getMacAddress ( destinationMAC ), getMacAddress ( sourceMAC ), socket.htons ( protocol ), data [ 14: ]

# Return a properly formated MAC address.
# bytesAddress is the address that it is broken up into chunk.
def getMacAddress ( bytesAddress ):
    # Convert each chunk into a string format.
    stringBytes = map ( '{:02x}'.format, bytesAddress )
    # Joins all the bytes together with ":" between all of then and makes an upper case.
    # Example: AA:BB:CC:DD:EE:FF:GG...
    return ':'.join( bytesAddress ).upper ( )
