import socket
import encryption
import struct

sTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'ii.virtues.fi'
PORT = 10000

remote_ip = socket.gethostbyname(HOST)

print 'IP address of ' + HOST + ' is ' + remote_ip

sTCP.connect((remote_ip, PORT))

print 'Socket Connected to ' + HOST + ' on IP ' + remote_ip

message = "HELO 10000\r\n"
#for i in range(20):
#    message = message + encryption.generateKey(64) + "\r\n"
#message = message + ".\r\n"

sTCP.sendall(message)

print 'To server: ' + message

reply = sTCP.recv(4096)

print 'Server reply: ' + reply

sTCP.close()

PORT = int(reply.split()[1])

print PORT

sUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sUDP.sendto('Ekki-ekki-ekki-ekki-PTANG.', (HOST, PORT))

d = sUDP.recvfrom(1024)
print d
