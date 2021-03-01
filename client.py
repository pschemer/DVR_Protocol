import json
import socket

class MyClient:
    def __init__(self, id, dv):
        ClientSocket = socket.socket()
        host = '127.0.0.1'
        port = 4550 + id

        try:
            ClientSocket.connect((host, port))
        except socket.error as e:
            print(str(e))

        payload = json.dumps(dv)
        ClientSocket.send(str.encode(payload))
        ClientSocket.send(str.encode(""))
        Response = ClientSocket.recv(1024)
        res = Response.decode()
        # Loop until server confirms receipt
        while res != 'OK':
            pass
        # Close this socket
        ClientSocket.close()
