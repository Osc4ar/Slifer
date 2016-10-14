from ethernetFrame import *
import socket

def rawSocket ( ):

    # Family, type, and protocol: The last parameter makes the socket compatable with all machines,
    # big endian or little endian it's correct for read, etc...
    RawSocket = socket.socket ( socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs ( 3 ) );

    # Main loop, listen for any data that comes across.
    while True:
        # rawData: Passing from the ethernet frame.
        # address: Source address.
        rawData, address = RawSocket.recvfrom ( 65536 );

        destinationMAC, sourceMAC, protocol, data = ethernetFrame ( rawData )

        print ('\nEthernet frame: ')
        print ('Destination: {}, source: {}, protocol: {}'.format ( destinationMAC, sourceMAC, protocol ))
