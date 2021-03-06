from gc import freeze
import socket
import threading
import time, copy
from pip import List

HEADER = 64
PORT = 5052
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
shotServer = "localhost"
shotPort = 5053
        
def receiveSenderMessage(conn):
    msg = ''
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
    
    return msg

def makeDataString(listEl: List):
    
    strData = ''
    freezeList = listEl.copy()
    print('---List before:')
    print(listEl)
    for i in range(len(freezeList)):
        strData += freezeList[i]
        if i != (len(freezeList) - 1):
            strData += ';'
    print('---ListAfter:')
    print(listEl)
    return strData, freezeList

def deleteElements(freezeList: List, listEls):
    
    for i in range(len(freezeList)):
        listEls.remove(freezeList[i])

def sendToReader(cli, listEl):
    
    msg, currentList = makeDataString(listEl)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    try:
        cli.send(send_length)
        cli.send(msg.encode(FORMAT))
        deleteElements(currentList, listEl)
        return True
    except:
        print("Cant send, Reader unavailable at this time.")
        return False
    
def setupClient():
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((shotServer, shotPort))
    except:
        print('Connect to the Reader component unsuccessfull.')
        client = None
    return client

def periodicSend(listEl):
    
    client = setupClient()
    while True:
        sent = sendToReader(client, listEl)
        if sent == False: client = setupClient()
        time.sleep(5)
        
def setupServer():
    print("[STARTING] server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    
    return server
                    
if __name__ == "__main__": # pragma: no cover
    
    listEl = []
    sendThread = threading.Thread(target=periodicSend, args=(listEl, ))
    
    server = setupServer()
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, addr = server.accept()
    print(f"Replicator sender accepted.")
    print(f"[NEW CONNECTION] {addr} connected.")
    sendThread.start()
    
    while True:
        msg = receiveSenderMessage(conn)
        listEl.append(msg)
    