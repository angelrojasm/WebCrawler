import socket

HOST = '127.0.0.1'

PORT = 3000
InfoQueue = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mySocket:
    mySocket.bind((HOST, PORT))
    mySocket.listen()
    while True:
        server, address = mySocket.accept()
        with server:
            print('Connected By', address)
            while True:
                data = server.recv(1024)
                message = data.decode('utf-8')
                if not data:
                    break
                if(message == 'worker-request'):
                    print(
                        'Server recieved request from Worker. Sending Queue Position:')
                    if(len(InfoQueue) == 0):
                        print('queue is empty')
                        server.sendall(b'0')
                    else:
                        server.sendall(str.encode(InfoQueue[0]))
                        InfoQueue.pop(0)
                else:
                    print('Server recieved data from client')
                    print(message)
                    InfoQueue.append(message)
