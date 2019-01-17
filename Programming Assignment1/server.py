#!/usr/bin/env python
"""
TCP Version
"""
import socket
import os.path
import sys



# create the socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# to see if the parameters you pass are correct
if len(sys.argv) < 2:
    print "Missing parameters, please add port number!"
    exit(1)

# pass in port number
portnumber = sys.argv[1]

#print out my host name
print socket.gethostname()

# bind to an address and port
serversocket.bind((socket.gethostname(), int(portnumber)))

# start listening up to 5 client without queueing
serversocket.listen(5)

# accept connections from client
(clientsocket, address) = serversocket.accept()
print "Get a client connected from ", address

# if get the connection from client either response requested file or save PUT file to disk etc..
while 1:
        #receive the http request message from the client
        data = clientsocket.recv(1024)
        # split the request message and parse the message we want
        datalist = data.split(' ')

         # give  server path
        path = "/home/wliang/server/"

        #if the request message is GET request
        if data[0:3] == 'GET':

            #datalist[1] is the file requested by the client(index.html),append it to the server path
            filepath = path+str(datalist[1])

            # test whether the file exist
            if os.path.isfile(filepath):
                #if file exist, send the request file to client
                print "GET request, file Exist, return 200 to client side!"
               # clientsocket.send("200 OK    client receive the file now\n")
                #clientsocket.send("\r\n")
                file = open(filepath, "rw+")
                content = file.read()
                clientsocket.send(str(content))
                file.close()
                #break

            else:
                #if file is not exist,give a message
                clientsocket.send("404 Not Found\n")
                #break
        #if the request message is PUT request, response message to client, let
        #client send the file to server via socket, and server save the file to disk
        elif data[0:3] == 'PUT':
            print 'PUT request, recevive file from client side'
            clientsocket.send('PUT')
            filepath = path + str(datalist[1])
            file = open(filepath, "w")
            data2 = clientsocket.recv(4096)
            print filepath
            print str(data2)
            file.write(str(data2))
            file.close()

            #break
        else:
              # else if the request is invalid form of request
              print "Invalid form of request from the client"
              #break

clientsocket.close()
