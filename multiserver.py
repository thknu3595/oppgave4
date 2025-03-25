
from socket import *
import _thread as thread
import time
import sys

def now():

    """returnerer tiden"""

    return time.ctime(time.time())

def handleClient(connection):

    """En funksjon som brukes som klient håndtør"""

    while True:
        data = connection.recv(1024).decode()
        print ("received  message = ", data)
        modified_message= data.upper()
        connection.send(modified_message.encode())
        if (data == "exit"):
            break
    connection.close()


def main():
    """
    Oppretter en server-socket, lytter etter nye tilkoblinger,
    og oppretter en ny tråd hver gang en ny tilkobling opprettes.
    """
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    try:
        serverSocket.bind(('',serverPort))

    except:
        print("Binding feilet . Error : ")
        sys.exit()
    serverSocket.listen(1)
    print ('Serveren er klar til å motta meldinger')
    while True:
        connectionSocket, addr = serverSocket.accept()
        print('Serveren er tilknyttet til ', addr)
        print('på ', now())
        thread.start_new_thread(handleClient, (connectionSocket,))
    serverSocket.close()

if __name__ == '__main__':
    main()



