import socket
import struct
import textwrap

# Unpack IPv4.
def IPHeader ( data ):
    versionLength = data [ 0 ]
    # Remember that the first 2 bytes of the header are "0000".
    version = versionLength >> 4
    # Take the version length and ended with 15 bytes.
    headerLength = ( versionLength & 15 ) * 4
    # Line 14 take a chunk of binary and stract that binary into the variables.
    # For the data the size is 20 bytes ( data [ : 20 ] ).
    # TTL is the time to live.
    TTL, protocol, source, target = struct.unpack ( '! 8x B B 2x 4s 4s', data [ :20 ] )

    return version, headerLength, TTL, protocol, IPv4 ( source ), IPv4 ( target ), data [ headerLength: ]

# Return a properly formating IPv4 address.
# address is the data that it is broken up into chunk.
def IPv4 ( address ):
    # Convert all the chunk ( address ) into a string and join it together with a colon in the middle.
    return ':'.join ( map ( str, address ) )

# The protocol tell us what kind of data it's caring ( TCP, UDT, ect... ).
# Unpack ICMP packet.
def packetICMP ( data ):
    # Grab the first 4 bytes and return to the variables.
    typeICMP, code, checksum = struct.unpack ( '! B B H', data [ :4 ] )
    return typeICMP, code, checksum, data [ 4: ] # data [ 4: ] read: data four to the end.

# Unpack TCP packet.
def segmentTCP ( data ):
    # Chunck of 16 bytes:
    ( sourcePort, destinationPort, sequence, acknowledgement, offsetReservedFlags ) = struct.unpack ( '! H H L L H', data [ :16 ] )
    # The offset, reserved, TCP flags, are all in one chunk. So we need to unpack thoose 16 bytes.
    offset = ( offsetReservedFlags >> 12 ) * 4
    # Base connection flags. ( ACK, SYN, FIN, ect... ).
    flagsURG = ( offsetReservedFlags & 32 ) >> 5
    flagsACK = ( offsetReservedFlags & 16 ) >> 4
    flagsPSH = ( offsetReservedFlags & 8 ) >> 3
    flagsRST = ( offsetReservedFlags & 4 ) >> 2
    flagsSYN = ( offsetReservedFlags & 2 ) >> 1
    flagsFIN = offsetReservedFlags & 1

    return sourcePort, destinationPort, sequence, acknowledgement, flagsURG, flagsACK, flagsPSH, flagsRST, flagsSYN, flagsFIN, data [ offset: ]

# Unpack UDP packet.
def segmentUDP ( data ):
    # chunk of 8 bytes.
    sourcePort, destinationPort, size = struct.unpack ( '! H H 2x H', data [ :8 ] )
    return sourcePort, destinationPort, size, data [ 8: ]

# Found this online ( jaja ).
# Formats multi-line data.
def formatMulti_Line ( prefix, string, size = 80 ):
    size -= len ( prefix )
    if isinstance ( string, bytes ):
        string = ''.join ( r'\x{:02x}'.format ( byte ) for byte in string )
        if size % 2:
            size -= 1
    return '\n'.join ( [ prefix + line for line in textwrap.wrap ( string, size ) ] )
