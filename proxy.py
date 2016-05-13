import socket
import sys
import select



def main():
    CONNECTION_LIST = []
    HOST = ''
    PORT = 40500
    RECV_BUFFER = 4096
    sTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sTCP = sTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sTCP.bind((HOST, PORT))
    print "Proxy online. Waiting for connections."
    sTCP.listen(2)
    
    CONNECTION_LIST.append(sTCP)
    print "Server started on port " + str(PORT)
    while True:
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])
        for sock in read_sockets:
            if sock == sTCP:
                sockfd, addr = sTCP.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                sockfd.sendall("Welcome to the server!")
            else:
                data = sock.recv(RECV_BUFFER)
                if data:
                    print "From (%s, %s) : " % addr + data
                    sock.sendall("That's fantastic!")
                    sForward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    host = socket.gethostbyname('ii.virtues.fi')
                    print host
                    sForward.connect((host, 10000))
                    sForward.sendall(data)
                    reply = sForward.recv(4096)
                    sock.sendall(reply)
                else:
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting down."
        sys.exit(1)
