import sys
import socket
import encryption
import struct
from questions import answer

def main():

    sUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    UDP_port = 10000
    
    while True:
        try: 
            sUDP.bind(('', UDP_port))
            break
            
        except socket.error, msg:
            if (UDP_port < 10101):
                UDP_port = UDP_port + 1
            else:
                print("Socket error with UDP bind", msg)
                break
    
    host = socket.gethostbyname('ii.virtues.fi')
    my_ip = socket.gethostbyname(socket.gethostname())

    key_table = []
    for i in range(20):
        key_table.append(encryption.generateKey(64))
            
    sTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sTCP.connect((host, 10000))
    helo_msg = "HELO " + str(UDP_port) + " C\r\n"
    for i in range(len(key_table)):
        helo_msg = helo_msg + key_table[i] + "\r\n"
    helo_msg = helo_msg + ".\r\n"
    
    print helo_msg
        
    sTCP.sendall(helo_msg)
    

    reply = sTCP.recv(1024)
    key_list = sTCP.recv(4096)
    port = int(reply.split()[1])
    print(reply, "port", port)
    #print "key list before modification"
    #print key_list
    key_list = key_list.split()[:-1]
    #print "server send:"
    #print key_list
    
    #Apparently we can't use two sockets here for UDP
    #sUDP_tosend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ini_msg = "Ekki-ekki-ekki-ekki-PTANG."
    data = struct.pack("!??HH64s", False, True, len(ini_msg), 0, ini_msg)
    
    sUDP.sendto(data, ((host, port)))
    print("udp message should be sent now")
    
    i = 0
    while True:
        reply2, addr = sUDP.recvfrom(4096)

        #print reply2
        uncoded = struct.unpack("!??HH64s", reply2)
        #print "uncoded"
        #print uncoded

        EOM = uncoded[0]
        print
        print "EOM is:", EOM

        question = uncoded[4].strip('\x00')
        
        if not EOM:
            print ""
            print "question:"
            print question
        
            decrypted = encryption.decrypt(question, key_list[i])
            
            print decrypted
            
            answ = answer(decrypted)

            print ""
            print "answer:"
            print answ
            
            crypted_answ = encryption.encrypt(answ, key_table[i+1])
            print crypted_answ
            
            data = struct.pack("!??HH64s", False, True, len(answ), 0, crypted_answ)
            sUDP.sendto(data, ((host, port)))
            
            #print "sent: " + data
            
            
            i = i + 1
        else:
            print question
            break
        #EOM = True

    sUDP.close()
    sTCP.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Shutting down"
        sys.exit(1)
