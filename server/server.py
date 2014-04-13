#!/usr/bin/python

import random
import socket
import time
import json

clients = {}

host = ''
port = 50000
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(backlog)
while True:

    client, address = s.accept()
    data = client.recv(size)
    if data:
        data_dict = json.loads(data)
        print data_dict
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
            clients[value]['message'] = {}
            clients[value]['latest'] = time.time()
        elif data_dict['username'] in clients and clients[data_dict['username']]['token'] == data_dict['token']:


            # Authenticated
            #print "Authenticated"

            clients[data_dict['username']]['latest'] = time.time()

            pieces = data_dict['data'].split(' : ')

            if pieces[0] == 'msg' and pieces[1] in clients:
                clients[pieces[1]]['message'][str(time.time())] = data_dict['username'] + ":" + pieces[2]
            elif pieces[0] == 'inbox':
                messages = clients[data_dict['username']]['message']

                output_data = ""
                for key in sorted(messages.keys()):
                    output_data += "\n%s" % (messages[key])
                

                #output_data = "\n".join(messages.values())

                clients[data_dict['username']]['message']={}
            else:

                clients[data_dict['username']]['x'] = data_dict['x']
                clients[data_dict['username']]['y'] = data_dict['y']
                clients[data_dict['username']]['shooting'] = data_dict['shooting']
                clients[data_dict['username']]['action'] = data_dict['action']

                output_data = clients
                #del output_data[data_dict['username']]
                output_data = json.dumps(output_data)



                

        else:
            output_data = "unknown"

        client.send(output_data)
    client.close() 
