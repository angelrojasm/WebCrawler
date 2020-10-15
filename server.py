import socket
import converter

HOST = '127.0.0.1'

PORT = 3000
# Queue for storing links
InfoQueue = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mySocket:
    mySocket.bind((HOST, PORT))
    mySocket.listen()
    while True:
        # always accepting connections
        server, address = mySocket.accept()
        with server:
            print('Connected By', address)
            while True:
                # Decodes data to parse messages
                data = server.recv(10000)
                message = data.decode('utf-8')
                print(message)
                if not data:
                    break

                if(converter.decodeToValues(message)[0] == "GetWork"):
                    print(
                        'Server recieved Get Request. Sending Queue front item info:')
                    if(len(InfoQueue) == 0):
                        # If queue is empty crawling is finished, sends message to worker to delete visited sites list
                        print('queue is empty')
                        server.sendall(str.encode('0'))
                    else:
                        server.sendall(str.encode(InfoQueue[0]))
                        InfoQueue.pop(0)
                else:
                    if(converter.decodeToValues(message)[0] == "PutWork"):
                        print('Server recieved data from client')
                        InfoQueue.append(message)
                        print('info queue is\n')
                        print(InfoQueue)
