#!/usr/bin/python
import os, sys
sys.path.append(os.path.abspath(os.path.join("..", "shared_modules")))

import socket
import threading
import json
import random
import vectors

def listenForClients(sock):
    # create an empty dictionary of clients
    clients = {}
    # start an infinite loop
    while True:
        # wait for a new client
        # when a client connects create a socket for responding to it called client
        client, address = sock.accept()
        # set the timeout to 5 seconds
        # If a client doesn't talk for 5 seconds it is deemed dead
        # and will be disconected
        client.settimeout(5)
        # start a new thread for the client to listen for
        # incoming messages and send back responses
        threading.Thread( target = listenToClient, args = (client,address, clients) ).start()

def listenToClient(client, address, clients):
    # set the buffer size for recieving data from the client
    size = 1024
    # start an infinite loop
    while True:
        try:
            print 'in loop'
            # get/wait for data from the client
            data = client.recv(size)
            
            if data:
                # data should be a json string so convert it to a dictionary
                data_dict = json.loads(data)
                print data
                # initialize output_data to an empty string
                output_data = ""
                # if the client is asking for a handshake check that it is
                # new client and send it back a token for authentication
                if data_dict['a'] == "handshake" and not data_dict['u'] in clients.keys():
                    # generate the token
                    token = "%f" % (random.random())
                    output_data = token
                    
                    # initialize
                    clients[data_dict['u']] = {}
                    # bind the generated token to the client
                    clients[data_dict['u']]['t'] = token
                    clients[data_dict['u']]['x'] = 0
                    clients[data_dict['u']]['y'] = 0
                    clients[data_dict['u']]['s'] = "none"
                    clients[data_dict['u']]['a'] = "none"

                elif data_dict['u'] in clients and clients[data_dict['u']]['t'] == data_dict['t']:
                    # Authenticated user with token
                    # update stored location and actions
                    # based on client data
                    # TODO: trust the client less. Add checking here...
                    clients[data_dict['u']]['x'] = data_dict['x']
                    clients[data_dict['u']]['y'] = data_dict['y']
                    clients[data_dict['u']]['s'] = data_dict['s']
                    clients[data_dict['u']]['a'] = data_dict['a']
                    output_data = json.dumps(clients)
                else:
                    # we didn't get data, probably because sock.recv
                    # timed out so raise an error to disconnect the client
                    # raise error('Client disconnected')
                    print 'Client disconnected'
                # debugging
                print output_data
                # send response to the client
                client.send(output_data)
            else:
                # if we didn't get data assume the client exploded
                # and raise an error
                raise error('Client disconnected')
        except:
            # if anything went wrong, cut off the client
            client.close()
            
            # end the thread
            return False

def main(host, port):
    # create the listening socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind the socket to the specified port and all interfaces
    sock.bind((host, port))
    sock.listen(5)
    # call listenForClients passing in the socket
    listenForClients(sock)
    
if __name__ == "__main__":
    # If we are being run directly, ask for a port and run
    # main() to listen on that port on all interfaces
    port = raw_input("Port? ")
    main('',int(port))
