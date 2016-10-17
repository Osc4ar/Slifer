from ethernetFrame import *
from IPHeader import *
import socket

DATAFORMAT_1 = '\t '
DATAFORMAT_2 = '\t\t '
DATAFORMAT_3 = '\t\t\t '

def rawSocket ( ):

    # Family, type, and protocol: The last parameter makes the socket compatable with all machines,
    # big endian or little endian it's correct for read, etc...
    RawSocket = socket.socket ( socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs ( 3 ) );

    # Main loop, listen for any data that comes across.
    while True:
        # rawData: Passing from the ethernet frame.
        # address: Source address.
        rawData, address = RawSocket.recvfrom ( 65536 );

        destinationMAC, sourceMAC, ethernetProtocol, data = ethernetFrame ( rawData )

        print ( '\nEthernet frame: ' )
        print ( 'Destination: {}, source: {}, Protocol: {}'.format ( destinationMAC, sourceMAC, ethernetProtocol ) )

        # 8 for IPv4 ( regular internet trafic ).
        if ethernetProtocol == 8:
            ( version, headerLength, TTL, protocol, source, target, data ) = IPHeader ( data )
            print ( 'IPv4 packet:' )
            print ( 'Version: {}, Header Length: {}, TTL: {}'.format ( version, headerLength, TTL ) )
            print ( 'Protocol: {}, Source: {}, Target: {}'.format ( protocol, source, target ) )

            # ICMP packet inside protocol.
            if protocol == 1:
                ( typeICMP, code, checksum, data ) = packetICMP ( data )
                print ( 'ICMP Packet: {}, Code: {}, Checksum: {}'.format ( typeICMP, code, checksum ) )
                print ( 'Data:' )
                print ( format_multi_line ( DATAFORMAT_3, data ) )

            # TCP packet inside protocol.
            elif protocol == 6:
                ( sourcePort, destinationPort, sequence, acknowledgement, flagsURG, flagsACK, flagsPSH, flagsRST, flagsSYN, flagsFIN, data ) = segmentTCP ( data )
                print ( 'TCP segment:' )
                print ( 'Source Port: {}, Destination Port: {}'.format ( sourcePort, destinationPort ) )
                print ( 'Sequence: {}, Acknowledgement: {}'.format ( sequence, acknowledgement ) )
                print ( 'Flags:' )
                print ( 'URG: {}, ACK: {}, PSH: {}, RST: {}, SYN: {}, FIN: {}'.format ( flagsURG, flagsACK, flagsPSH, flagsRST, flagsSYN, flagsFIN ) )
                print ( 'Data:' )
                print ( format_multi_line ( DATAFORMAT_3, data ) )

            # UDP packet inside.
            elif protocol == 17:
                sourcePort, destinationPort, size, data = segmentUDP ( data )
                print ( 'UDP segment:' )
                print ( 'Source Port: {}, Destination Port: {}, Length: {}'.format ( sourcePort, destinationPort, size ) )

            # Other.
            else:
                print ( 'Data:' )
                print ( format_multi_line ( DATAFORMAT_2, data ) )

        else:
            print ( 'Data:' )
            print ( format_multi_line ( DATAFORMAT_1, data ) )
