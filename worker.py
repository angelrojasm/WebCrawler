import socket
import scraper
import converter

HOST = '127.0.0.1'
PORT = 3000

# list to validate that links that have already been visisted will not be sent over to the queue
VisitedLinks = []
keyword = ''
maxDepth = 0
message = ''
shouldStop = False


def socketGetWork():
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((HOST, PORT))
    while True:
        mySocket.sendall(str.encode(
            converter.encodeToXML('GetWork', '', '', 0)))
        print('Worker sent info to Server')
        data = mySocket.recv(1024)
        message = data.decode('utf-8')
        if(message == '0'):
            print('Queue is empty')
            VisitedLinks.clear()
            return message
        else:
            print('Recieved info queue from server')
            mySocket.close()
            return message


def socketPutWork():
    message = socketGetWork()
    if(message == '0'):
        return True
    link = converter.decodeToValues(message)
    keyword = link[2]
    # Verifies the link has not already been scraped
    if not(link[1] in VisitedLinks):
        if(len(VisitedLinks) == 0):
            linkTuple = scraper.getWebsiteLinks(link[1], link[2], link[3] + 1)
        else:
            linkTuple = scraper.getWebsiteLinks(
                link[1], link[2], link[3])
        VisitedLinks.append(link[1])
        for branchLink in linkTuple[0]:
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket.connect((HOST, PORT))
            if not(branchLink in VisitedLinks) and (linkTuple[1] >= 0):
                mySocket.sendall(str.encode(converter.encodeToXML(
                    'PutWork', branchLink, keyword, linkTuple[1])))
            mySocket.close()

    return False


# Begin Scraping websites with the url provided by the server
while True:
    shouldStop = socketPutWork()
    if(shouldStop):
        break
