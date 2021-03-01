import json
import socket
from _thread import *

class MyServer:
    def __init__(self, id, node):
        self.node = node
        ServerSocket = socket.socket()
        host = '127.0.0.1'
        port = 4550 + id
        self.ID = id
        try:
            ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))

        ServerSocket.listen(1)

        def threaded_client(connection):
            while True:
                data = connection.recv(1024)
                try:
                    d = json.loads(data.decode())
                except:
                    pass
                # parse data to use in Node update
                dv = []
                for i in range(len(d)):
                    dv.append(d[i])
                # send update Node
                if len(data) > 1:
                    self.node.updateDV(d)
                reply = 'OK'
                connection.sendall(str.encode(reply))
                if not data:
                    break
            connection.close()

        while True:
            Client, address = ServerSocket.accept()
            start_new_thread(threaded_client, (Client, ))
        ServerSocket.close()
