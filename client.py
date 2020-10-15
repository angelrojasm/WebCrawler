import socket
import sys
import converter

# constants for socket connection
HOST = '127.0.0.1'
PORT = 3000

# Sets up command line values for client request
tempArr = sys.argv
del tempArr[0]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mySocket:
    mySocket.connect((HOST, PORT))
    mySocket.sendall(str.encode(converter.encodeToXML(
        'PutWork', tempArr[0], tempArr[1], tempArr[2])))
