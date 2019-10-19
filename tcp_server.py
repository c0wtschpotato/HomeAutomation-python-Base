#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import sys
import os
import ConfigParser


config = ConfigParser.ConfigParser()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.107', 10000)



print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)
while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:

            data = connection.recv(32)

            try:
              print data.split("-")
              print data.split("-")[2]

            except:
              print "Error on writing split Data"

            if not data == "":


              config.read('cfg.ini')
              # config.add_section(data.split("-")[0])
              config.set(data.split("-")[0],data.split("-")[1],data.split("-")[2])
              with open('cfg.ini', 'w') as configfile:
                config.write(configfile)

            # except:
            #     print "Error on write file"
            # print >>sys.stderr, 'received '+str(data)
            if data:
                useless = "chunk"
                # print >>sys.stderr, 'sending data back to the client'
                # connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break

    finally:
        # Clean up the connection
        connection.close()



