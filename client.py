import socket
import sys
import json

# constants for socket connection
HOST = '127.0.0.1'
PORT = 3000

# Sets up command line values for client request
tempArr = sys.argv
del tempArr[0]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mySocket:
    mySocket.connect((HOST, PORT))
    mySocket.sendall(str.encode(json.dumps(
        {"Method": "PutWork", "URL": tempArr[0], "Keyword": tempArr[1], "Depth": tempArr[2]})))
