import sys
import socket
import encryption
import struct
from questions import answer

VERBOSE = False

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
    
    user_input = raw_input("\nGive address of the server you wish to communicate with\n\n>")
    host = socket.gethostbyname(user_input)
    #host = socket.gethostbyname('ii.virtues.fi')
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
    
    if VERBOSE:
        print helo_msg
        
    sTCP.sendall(helo_msg)
    
    reply = sTCP.recv(1024)

    key_list = sTCP.recv(4096)

    port = int(reply.split()[1])
    if VERBOSE:
        print(reply, "port", port)

    #print "key list before modification"
    #print key_list
    key_list = key_list.split()[:-1]
    #print "server send:"
    #print key_list
    
    ini_msg = "Ekki-ekki-ekki-ekki-PTANG."
    data = struct.pack("!??HH64s", False, True, len(ini_msg), 0, ini_msg)
    
    sUDP.sendto(data, ((host, port)))
    #print("udp message should be sent now")
    
    i = 0
    while True:
        reply2, addr = sUDP.recvfrom(4096)

        uncoded = struct.unpack("!??HH64s", reply2)
        #print "uncoded"
        #print uncoded

        EOM = uncoded[0]
        
        
        question = uncoded[4].strip('\x00')
        
        if not EOM:

            if VERBOSE:
                print "\nQuestion " + str(i+1) +  ", EOM is:", EOM


            decrypted = encryption.decrypt(question, key_list[i])
            
            print "\nQuestion " + str(i+1) +  " from server"
            print decrypted
            
            answ = answer(decrypted)

            print "\nOur answer:"
            print answ
            
            crypted_answ = encryption.encrypt(answ, key_table[i+1])
            #print crypted_answ
            
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

# Forgot bout the argparse module, oh well.
def printHelp():
    print "\nAvailable parameters for this script are :\n"
    print "Verbose     -v"
    print "Help        -h"
    print "Proxy       -p" # Might not need this here

if __name__ == '__main__':
    try:
        '''What format should we enforce?
                - python mainc.py ii.virtues.fi ?

           The nice thing bout that format would be that the address
           would always be in the same index of the argument vectors,
           and we wouldn't have to attempt to parse it out. 
           Timo make a call. Force sys.argv[1] to be either ii.virtues.fi,
           localhost or proxy?

           Never mind, use raw_input to ask user for address.
        '''
        for i in range(len(sys.argv)):
            
            #if len(sys.argv) < 2:
            #    print "\nYou didn't give sufficient arguments for this script!"
            #    printHelp()
            #    sys.exit(1)

            if "-help" in sys.argv:
                printHelp()
                sys.exit(1)

            if "-h" in sys.argv:
                printHelp()
                sys.exit(1)

            if "-v" in sys.argv:
                VERBOSE = True
            else:
                VERBOSE = False

            if "-p" in sys.argv:
                pass
                # Do something to toggle proxy, maybe with flag such as with verbose

        '''I guess this is still an option, just not a real good one,
        program might throw errors if user doesn't know correct input format.''' 
        #address = sys.argv[1] 
        #main(address)
        main()
    except KeyboardInterrupt:
        print "Shutting down"
        sys.exit(1)
