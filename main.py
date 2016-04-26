import socket
import encryption
import struct

def main():

    sUDP_torecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sUDP_torecv.bind(('', 10000))
    
    host = socket.gethostbyname('ii.virtues.fi')
    print socket.gethostbyname(socket.gethostname())
    
    sTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sTCP.connect((host, 10000))
    sTCP.sendall("HELO 10000\r\n")
    
    reply = sTCP.recv(1024)
    port = int(reply.split()[1])
    print reply
    
    sUDP_tosend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ini_msg = "Ekki-ekki-ekki-ekki-PTANG."
    
    data = struct.pack("!??HH64s", False, True, len(ini_msg), 0, ini_msg)
    sUDP_tosend.sendto(ini_msg, ((socket.gethostname(), 10001)))
    print data
    
    reply, addr = sUDP_torecv.recvfrom(1024)
    print "%s from %s" % (reply, addr)

    sUDP_torecv.close()
    sUDP_tosend.close()
    sTCP.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting down"
        sys.exit(1)
