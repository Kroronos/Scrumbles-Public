#!/usr/bin/python3

import socket, sys, threading, threadServer
from struct import *

changeString = '<change>'
MSGLEN = len(changeString)
dbMon = threadServer.dbMonitor()


def mainLoop():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except socket.error:
        print('Socket not created.  : ')
        sys.exit()

    while True:
        packet = s.recvfrom(65565)
        packet = packet[0]

        ip_header = packet[0:20]

        iph = unpack('!BBHHHBBH4s4s', ip_header)

        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF

        iph_length = ihl * 4

        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8])
        d_addr = socket.inet_ntoa(iph[9])

        
        tcp_header = packet[iph_length:iph_length+20]
        tcph = unpack('!HHLLBBHHH', tcp_header)

        source_port = tcph[0]
        dest_port = tcph[1]
        sequence = tcph[2]
        ack = tcph[3]
        doff_reserved =  tcph[4]
        tcph_length = doff_reserved >> 4
    

        if dest_port == 3306:
            h_size = iph_length + tcph_length*4
            data = packet[h_size:]
            data_size = len(packet) - h_size
            searchList = [b'INSERT',b'DELETE',b'UPDATE',b'DROP',b'insert',b'delete',b'update',b'drop']
            if any(s in data for s in searchList):
                #print('Database change occured')
                dbMon.postChange()


server = threadServer.ThreadedServer(5005,dbMon)
threading.Thread(target = mainLoop, args=()).start()
threading.Thread(target = server.listen, args=()).start()
