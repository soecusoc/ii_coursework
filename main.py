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
    helo_msg = "HELO " + str(UDP_port) + " MC\r\n"
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
    if VERBOSE:
        print("udp message should be sent now")
    
    def parseMultipart(j):
        print "\nparseMultipart\n"

        ret = ""
        _continue = True

        while _continue:
            
            reply2, _addr = sUDP.recvfrom(200)

            uncoded = struct.unpack("!??HH64s", reply2)


            uncrypted_question = uncoded[4].strip('\x00')

            decrypted = encryption.decrypt(uncrypted_question, key_list[j])
            
            print "\ndecrypted"
            print decrypted

            ret = ret + decrypted
            print "\nret"
            print ret
            j = j + 1
            if uncoded[3] == 0:
                _continue = False

        if uncoded[0] == False:
            
            #print "EOM is false"
            return (ret, _addr, False)

        else:
            #print "EOM is true"
            return (ret, _addr, True)

    
    i = 0
    while True:

        question, addr, EOM = parseMultipart(i)

        if not EOM:

            if VERBOSE:
                print "\nQuestion " + str(i+1) +  ", EOM is:", EOM

            print "\nQuestion " + str(i+1) +  " from server"
            print question

            count = question.count('?')

            print "count"
            print count

            if count > 1:
                question = question.split('?')


                answers = ""

                x = count 
                for n in range(x):


                    _question = question[n] + "?"

                    print "Question"
                    print _question

                    answ = answer(_question)

                    print "\nOur answer:"
                    print answ
                    
                    answers = answers + answ

                    #crypted_answ = encryption.encrypt(answ, key_table[i+1])
                    #print crypted_answ
                    
                    #data = struct.pack("!??HH64s", False, True, len(answ), 0, crypted_answ)
                    #sUDP.sendto(data, ((host, port)))
                    
                    #print "sent: " + data
                    i = i + 1

                size = sys.getsizeof(answers)

                #print "size"
                #print size

                temp2 = ""

                if size > 64:

                    for k in range(len(answers)):

                        temp2 = temp2 + answers[k]

                        if sys.getsizeof(temp2) == 64:

                            crypted_answ = encryption.encrypt(temp2, key_table[i+1])
                            data = struct.pack("!??HH64s", False, True, len(answ), 0, crypted_answ)
                            sUDP.sendto(data, ((host, port)))

                            temp2 = ""

                    crypted_answ = encryption.encrypt(temp2, key_table[i+1])
                    data = struct.pack("!??HH64s", False, True, len(answ), 0, crypted_answ)
                    sUDP.sendto(data, ((host, port)))


                    #crypted_answ = encryption.encrypt(answ, key_table[i+1])
                break
            else:

                answ = answer(question)

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
    print "Help        -h, -help"

if __name__ == '__main__':
    try:

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


        '''I guess this is still an option, just not a real good one,
        program might throw errors if user doesn't know correct input format.''' 
        #address = sys.argv[1] 
        #main(address)
        main()
    except KeyboardInterrupt:
        print "Shutting down"
        sys.exit(1)
