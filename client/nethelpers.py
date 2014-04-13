import socket
import json
class server(object):
    def __init__(self, server_ip, server_port):
        self.ip = server_ip
        self.port = server_port
        
    def handshake(self, username):
        token = self.sendToServer({"username": username, "action": "handshake"})
        return token
    
    
    def sendToServer(self, input_dict):
        host = self.ip
        port = int(self.port)
        size = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        s.send(json.dumps(input_dict))
        data = s.recv(size)
        s.close()
        return data
    """
    def getInbox(username, token):
        return sendToServer({"username": username, "token": token, "data": "inbox", "action": "none"})
    """
