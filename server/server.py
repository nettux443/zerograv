#!/usr/bin/python

import socket
import threading
import time
import json
import random

def listenForClients(sock):
    clients = {}
    while True:
        client, address = sock.accept()
        threading.Thread( target = listenToClient, args = (client,address, clients) ).start()

def listenToClient(client, address, clients):
    size = 1024
    while True:
        try:
            data = client.recv(size)
            if data:

                data_dict = json.loads(data)
                #print data_dict
                output_data = ""
                if data_dict['action'] == "handshake":
                    value = data_dict['username']
                    token = "%f" % (random.random())
                    output_data = str(token)
                    #print "%s connected with token: %s" % (value, token)
                    clients[value] = {}
                    clients[value]['token'] = token
                    clients[value]['x'] = 0
                    clients[value]['y'] = 0
                    clients[value]['shooting'] = "none"
                    clients[value]['action'] = "none"
                elif data_dict['username'] in clients and clients[data_dict['username']]['token'] == data_dict['token']:
                    # Authenticated

                    pieces = data_dict['data'].split(' : ')
                    clients[data_dict['username']]['x'] = data_dict['x']
                    clients[data_dict['username']]['y'] = data_dict['y']
                    clients[data_dict['username']]['shooting'] = data_dict['shooting']
                    clients[data_dict['username']]['action'] = data_dict['action']
                    output_data = json.dumps(clients)
                else:
                    output_data = "unknown"
                print output_data
                client.send(output_data)
            else:
                raise error('Client disconnected')
        except:
            client.close()
            return False

def main(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    listenForClients(sock)
    
if __name__ == "__main__":
    port = raw_input("Port? ")
    main('',int(port))
