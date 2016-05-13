import socket
import sys
import struct

def bindsocket(type):

    if type == "TCP":
        connection = socket.SOCK_STREAM
    elif type == "UDP":
        connection = socket.SOCK_DGRAM
    else:
        print "Invalid socket connection type."
        return -1

    s = socket.socket(socket.AF_INET, connection)
    
    port = 10000
    
    while True:
        try: 
            s.bind(('', port))
            break
            
        except socket.error, msg:
            if (port < 10101):
                port = port + 1
            else:
                print("Socket error with TCP bind", msg)
                break
                
    #print "%s-socket bound in port %d" % (type, port)
                
    return s, port

def main():

    forward_addr = socket.gethostbyname('ii.virtues.fi')

    my_ip = socket.gethostbyname(socket.gethostname())
    print "Proxy server online on IP-address %s." % my_ip
    print

    sTCP_client, TCP_port_client = bindsocket("TCP")
                
    sUDP, UDP_port = bindsocket("UDP")
    
    print "Waiting for TCP-connection from client on port %s." % TCP_port_client
    print
    print "Waiting for UDP-connection from client on port %s." % UDP_port
    print
    
    sTCP_client.listen(2)
    
    conn_client, addr_client = sTCP_client.accept()
    
    print "TCP-connection established from %s with port number %s." % addr_client
    print
    
    helo_msg = conn_client.recv(4096)
    
    print "Client:"
    print helo_msg
    print
    
    helo, key = helo_msg.split('\r\n', 1)
    helo_table = helo.split()
    data_port_to_client = int(helo_table[1])
    helo_table[1] = str(UDP_port)
    helo = helo_table[0] + " " + helo_table[1] + " " + helo_table[2] + "\r\n"
    helo_msg = helo + key
    
    TCP_port_server = 10000
    sTCP_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sTCP_server.connect((forward_addr, 10000))
    sTCP_server.sendall(helo_msg)
    
    print "Server:"
    print helo
    print key
    print

    helo = sTCP_server.recv(1024)
    key = sTCP_server.recv(4096)
    
    helo_table = helo.split()
    data_port_to_server = int(helo_table[1])
    helo_table[1] = str(UDP_port)
    helo = helo_table[0] + " " + helo_table[1] + " " + helo_table[2] + "\r\n"

    conn_client.sendall(helo)
    conn_client.sendall(key)
    
    while True:
        client_reply, client_addr = sUDP.recvfrom(4096)
        #EOM = struct.unpack("!??HH64s", client_reply)[0]
        #if EOM: break
        print "Client:", client_reply
        
        sUDP.sendto(client_reply, (forward_addr, data_port_to_server))
        
        server_reply, ser_addr = sUDP.recvfrom(4096)
        #EOM = struct.unpack("!??HH64s", server_reply)[0]
        #if EOM: break
        print "Server:", server_reply
        
        sUDP.sendto(server_reply, (my_ip, data_port_to_client))
    
    

    
    
    sTCP_client.close()
    sUDP.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting down."
        sys.exit(1)
