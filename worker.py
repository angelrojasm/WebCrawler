import socket

HOST = '127.0.0.1'

PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mySocket:
    mySocket.connect((HOST, PORT))
    mySocket.sendall(str.encode('worker-request'))
    print('Worker sent info to Server')
    data = mySocket.recv(1024)
    message = data.decode('utf-8')
    if(message == '0'):
        print('Queue is empty')
    else:
        print('Recieved info queue from server')
        print(message)
