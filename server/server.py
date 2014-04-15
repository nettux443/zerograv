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
                output_data = ""
                if data_dict['a'] == "handshake":
                    value = data_dict['u']
                    token = "%f" % (random.random())
                    output_data = token

                    clients[value] = {}
                    clients[value]['t'] = token
                    clients[value]['x'] = 0
                    clients[value]['y'] = 0
                    clients[value]['s'] = "none"
                    clients[value]['a'] = "none"
                elif data_dict['u'] in clients and clients[data_dict['u']]['t'] == data_dict['t']:
                    # Authenticated
                    clients[data_dict['u']]['x'] = data_dict['x']
                    clients[data_dict['u']]['y'] = data_dict['y']
                    clients[data_dict['u']]['s'] = data_dict['s']
                    clients[data_dict['u']]['a'] = data_dict['a']
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
