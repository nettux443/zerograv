import socket
import json

class server(object):
    def __init__(self, server_ip, server_port):
        # set up connection with the server
        self.ip = server_ip
        self.port = server_port
        # create the socket to use and say hi to the sever!
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip,int(self.port)))
        
    def handshake(self, username):
        # get a token from the server
        # this is just a random number but it serves as simple authentication
        token = self.sendToServer({"u": username, "a": "handshake"})
        return token
    
    def sendToServer(self, input_dict):
        # set the buffer size
        size = 1024
        # convert the dictionary into a json string and send it to the server
        self.sock.send(json.dumps(input_dict))
        # read and return the servver's response
        data = self.sock.recv(size)
        return data

    def close(self):
        # disconnect from the server
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip,int(self.port)))
        return True
