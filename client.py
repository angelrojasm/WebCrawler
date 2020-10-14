import socket
import sys

HOST = '127.0.0.1'
PORT = 3000

tempArr = sys.argv
del tempArr[0]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mySocket:
    mySocket.connect((HOST, PORT))
    mySocket.sendall(str.encode('info is ' + tempArr[0]))
    print('Client sent info to Server')
