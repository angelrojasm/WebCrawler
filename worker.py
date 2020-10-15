import socket
import scraper
import json

HOST = '127.0.0.1'
PORT = 3000

# list to validate that links that have already been visisted will not be sent over to the queue
VisitedLinks = []
keyword = ''
maxDepth = 0


def socketGetWork():
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((HOST, PORT))
    while True:
        mySocket.sendall(str.encode(json.dumps(
            {"Method": "GetWork", "URL": '', "Keyword": '', "Depth": 0})))
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
            if(message == '0'):
                return ('0', '0')
            else:
                return (message, json.loads(message)["Depth"])


def socketPutWork():
    global maxDepth
    tempTuple = socketGetWork()
    message = tempTuple[0]
    if(message == '0'):
        return True
    if(len(VisitedLinks) == 0):
        maxDepth = int(tempTuple[1])
    link = json.loads(message)
    keyword = link["Keyword"]
    # Verifies the link has not already been scraped
    if not(link["URL"] in VisitedLinks):
        if(len(VisitedLinks) == 0):
            linkTuple = scraper.getWebsiteLinks(
                link["URL"], link["Keyword"], 'Initial Link')

        else:
            linkTuple = scraper.getWebsiteLinks(
                link["URL"], link["Keyword"], link["Depth"])
        VisitedLinks.append(link["URL"])
        for branchLink in linkTuple[0]:
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket.connect((HOST, PORT))
            if not(branchLink in VisitedLinks) and (linkTuple[1] <= maxDepth):
                mySocket.sendall(str.encode(json.dumps(
                    {"Method": "PutWork", "URL": branchLink, "Keyword": keyword, "Depth": linkTuple[1]})))
            mySocket.close()

    return False


# Begin Scraping websites with the url provided by the server
while True:
    shouldStop = socketPutWork()
    if(shouldStop):
        break
