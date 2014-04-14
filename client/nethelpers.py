import socket
import json

class server(object):
    def __init__(self, server_ip, server_port):
        self.ip = server_ip
        self.port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip,int(self.port)))
        
    def handshake(self, username):
        token = self.sendToServer({"username": username, "action": "handshake"})
        return token
    
    
    def sendToServer(self, input_dict):
        size = 1024
        self.sock.send(json.dumps(input_dict))
        data = self.sock.recv(size)
        return data

    def close(self):
        self.sock.close()
        return True
