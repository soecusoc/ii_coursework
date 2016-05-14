'''
This proxy works with Confidentiality feature.
Doesn't support plain, featureless main.
Should work with Multipart feature also, but haven't been tested with it.
'''
import socket
import sys
import struct

BUFFERSIZE = 4096
PORT = 10000

def gethostnamefromcommandline():
    #Check validness of commandline arguments.
    #Asks address from keyboard if connection cannot be established.
    name = sys.argv[0]

    if len(sys.argv) != 2:
        print "Usage: %s <server address>" % name
        sys.exit(1)

    address = sys.argv[1]
        
    bad_address = True
    while bad_address:
        try:
            ip = socket.gethostbyname(address)
            bad_address = False
        except socket.gaierror:
            print "Error: Cannot connect to \"%s\"." % address
            print "Please try again or give \"q\" to quit."
            address = raw_input("> ")
            
        if address == "q":
            print "Shutting down."
            sys.exit(1)
    
    return ip

def bindsocket(type):
    #Creates and binds a TCP or a UDP socket to the first free port in range 10000-10100
    #Doesn't define address in any way.
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
                print("Socket error with bind", msg)
                break
                                
    return s, port
    
def processhelomessage(raw_helo, port):
    #Replaces the port in helo message with proxy server's own port
    helo_table = raw_helo.split()
    port_to_forward = int(helo_table[1])
    helo_table[1] = str(port)
    helo = helo_table[0] + " " + helo_table[1] + " " + helo_table[2] + "\r\n"
    
    return helo, port_to_forward
    
def forwarddatagrams(sUDP, server_ip, server_port, client_ip, client_port):
    #Forwards messages from client to server and from server to client.
    #Checks for eom in both message.
    data, addr = sUDP.recvfrom(BUFFERSIZE)
        
    unpacked = struct.unpack("!??HH64s", data)
    EOM = unpacked[0]
        
    if addr[0] == server_ip:
        print "Server:", data
        print "Forwarding to client."
        print
        sUDP.sendto(data, (client_ip, client_port))
        
    if addr[0] == client_ip:
        print "Client:", data
        print "Forwarding to server."
        print
        sUDP.sendto(data, (server_ip, server_port))

    return EOM

def main():

    server_ip = gethostnamefromcommandline()

    my_ip = socket.gethostbyname(socket.gethostname())
    print "Server online on IP-address %s." % my_ip
    print

    sTCP_client, TCP_port_client = bindsocket("TCP")
    sUDP, UDP_port = bindsocket("UDP")
    
    print "Waiting for TCP-connection from client on port %s." % TCP_port_client
    
    sTCP_client.listen(2)
    
    conn_client, client_addr = sTCP_client.accept()
    sTCP_client.close()
    
    print "TCP-connection established from %s with port number %s." % client_addr
    print
    
    helo_msg = conn_client.recv(BUFFERSIZE)
        
    helo, key = helo_msg.split('\r\n', 1)
    helo, data_port_to_client = processhelomessage(helo, UDP_port)
    helo_msg = helo + key
        
    print "Ready to send datagrams to the client."
    
    sTCP_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sTCP_server.connect((server_ip, PORT))
    sTCP_server.sendall(helo_msg)

    helo = sTCP_server.recv(BUFFERSIZE)
    key = sTCP_server.recv(BUFFERSIZE)
    
    helo, data_port_to_server = processhelomessage(helo, UDP_port)

    conn_client.sendall(helo)
    conn_client.sendall(key)
    
    conn_client.close()
    sTCP_server.close()
    
    print "Ready to send datagrams to the server."
    
    print
    
    client_ip = client_addr[0]
    
    EOM = False
    while not EOM:
       
       EOM = forwarddatagrams(sUDP, server_ip, data_port_to_server, client_ip, data_port_to_client)
            
    print "Session finished successfully."
    print "Shutting down the server."
    
    sUDP.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting down."
        sys.exit(1)
