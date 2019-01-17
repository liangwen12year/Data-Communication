#!/usr/bin/env python
"""
TCP Version
"""
import socket
import sys
import time



class Client:

    def __init__(self):
        # default parameter for client socket to initialize
        self.portnumber = 80
        self.host = 'wliang-ThinkPad-T450'
        self.command = 'GET'
        self.filename = 'index.html'

        # create the socket
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get parameter from command line(host, portnumber, command etc...)
    def getHost(self):
        self.host = sys.argv[1]

    def getPortNum(self):
        self.portnumber = int(sys.argv[2])

    def getCommand(self):
        self.command = sys.argv[3]

    def getFile(self):
        self.filename = sys.argv[4]

    def getParameters(self):
        if len(sys.argv) < 5:
            #command line exception handling
            print "Missing parameters,try again"
            raise RuntimeError("Exitting due to parameter...")
        # get necessary parameters from command line
        self.getPortNum()
        self.getHost()
        self.getCommand()
        self.getFile()

    #form the http request message
    def formRequest(self):
        request = ''
        if self.command == 'GET':
            request = 'GET /' + self.filename + ' HTTP/1.1\r\nHost: '+self.host+'\r\n\r\n'
        elif self.command == 'PUT':
            request = 'PUT ' + self.filename + ' HTTP/1.1\r\nHost: '+self.host+'\r\n\r\n'
        return request

    def initSocket(self):
        # connects to a webserver at port #
        self.clientsocket.connect((self.host, self.portnumber))

if __name__ == '__main__':
    myclient = Client()
    myclient.getParameters()
    #print the parameters that you pass in to make sure the program run correctly
    print myclient.host, myclient.portnumber, myclient.command, myclient.filename
    myclient.initSocket()
    msg = myclient.formRequest()

    # send request to server
    myclient.clientsocket.sendall(msg)



    # get response from the server
    response = myclient.clientsocket.recv(4096)

    # PRINT the response we get from the server
    print response

    #if the reponse we receive from server is 'PUT', which means server agree us to put file then we read the file and
    #send it to the server through the client socket
    if (response == 'PUT'):
        path = "/home/wliang/client/"
        filepath = path + myclient.filename
        print filepath
        file = open(filepath, "rw+")
        content = file.read()
        print str(content)
        myclient.clientsocket.sendall(str(content))
        file.close()

    #print out the requested html body
    while (len(response) > 0):
        response = myclient.clientsocket.recv(4096)
        print  response


    #close the client socket
    myclient.clientsocket.close()
