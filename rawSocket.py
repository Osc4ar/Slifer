import socket
import sys

def Main ( ):

    host = socket.gethostbyname ( socket.gethostname ( ) )
    puerto = 9709

    # Socket tipo TCP/IP.
    crearSocket = socket.socket ( socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP ) # Revisar IPPROTO_IP ya que a mi me marca error.

    try:
        # Asociamos el socket a una direccion y puerto de servidor.
        crearSocket.bind ( host, puerto )
    except scoket.error as e:
        print ( str ( e ) )

    # Incluir cabeceras IP.
    crearSocket.setsockopt ( socket.IPPROTO_IP, socket.IP_HDRINCL, 1 )

    # Recibe todos los paquetes.
    crearSocket.ioctl ( socket.SIO_RCVALL, socket.RCVALL_ON )

    # Imprime paquete recivido.
    print crearSocket.recvfrom ( 9709 )

Main ( )
