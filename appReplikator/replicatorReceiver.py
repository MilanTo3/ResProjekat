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

def handle_client(conn):
    
    while True:
        msg = receiveSenderMessage(conn, listEl)
        listEl.append(msg)
    
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
        listEl.remove(freezeList[i])
    print('---ListAfter:')
    print(listEl)
    return strData

def sendToReader(cli, listEl):
    
    msg = makeDataString(listEl)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    cli.send(send_length)
    cli.send(msg.encode(FORMAT))
    
def setupClient():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((shotServer, shotPort))
    return client

def periodicSend(listEl):
    
    #client = setupClient()
    
    while True:
        #sendToReader(client, listEl)
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
    handle_client(conn, addr)
    