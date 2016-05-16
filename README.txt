II coursework for group '); DROP TABLE ryhmät;

Authors:

Sami Lauri	samilaur@student.oulu.fi	1951815

Timo Lintonen	tlintone@student.oulu.fi	2192796

Jussi Sepponen	jseppone@student.oulu.fi	1981199


How to use the program:

1) Set up proxy server in the task-directory with the command

	- python proxy.py 'address'

where address is the server we want to communicate with, ii.virtues.fi. Leave this program running, it will print "Server online on IP-adress " followed by an IP-address.

2) Run the main program main.py in a separate console with the command

	- python main.py

The program will query you for an address, use the IP that proxy.py displayed for you, if you wish to use the proxy functionality, ii.virtues.fi if not.