#!./env/bin/python3

# Imports
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOL_SOCKET
from socket import SO_REUSEADDR
from threading import Thread
from threading import Lock
from sys import stdin
from sys import argv
from select import select
import time
from networkMessaging import encodeMessage
from networkMessaging import decodeMessage


# KeyValServer class extends the KeyValStoreServicer class
# serverAddress: (string) the local address of the server
# port: (int) the port number for tcp communications
class KeyValServer:
    def __init__(self, port):
        self.keyVal = {}
        self.keyValLock = Lock()
        self.serverAddress = "127.0.0.1"
        self.port = port
        self.bufferSize = 1024
        self.backlog = 10
        self.tcpSocket = None
        self.threads = []

    # OpenSockets opens the sockets for both TCP and UDP
    # and sets self.tcpSocket and self.udpSocket for the server
    def openSocket(self):
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        self.tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.tcpSocket.bind((self.serverAddress, self.port))
        self.tcpSocket.listen(self.backlog)

    # Handles a TCP Request by decoding the incoming message
    # completing the given request and sending an encoded message
    # back to the sender
    def handleRequest(self, connection, address):
        isRunning = True
        while isRunning:
            data = connection.recv(self.bufferSize)

            if not data:
                break
            inMessage = decodeMessage(data)
            outMessage = ""
            command = inMessage["command"]
            if command == "get":
                key = inMessage["key"]
                value = self.get(key)
                outMessage = encodeMessage(key=key, value=value, success=True)
            elif command == "put":
                key = inMessage["key"]
                value = inMessage["value"]
                success = self.put(key, value)
                outMessage = encodeMessage(key=key, value=value, success=success)
            elif command == "delete":
                key = inMessage["key"]
                success = self.delete(key)
                outMessage = encodeMessage(key=key, success=success)
            else:
                error = "No command called " + command
                outMessage = encodeMessage(success=False, error=error)
            connection.send(outMessage.encode("ascii"))
            isRunning = False
        connection.close()

    # The main loop for the server delagates handling of all requests
    def run(self):
        self.openSocket()
        inputs = [self.tcpSocket, stdin]
        isRunning = True
        while isRunning:
            readyInputs, readyOutputs, readyExcepts = select(inputs, [], [])
            for readyInput in readyInputs:
                if readyInput == self.tcpSocket:
                    connection, address = self.tcpSocket.accept()
                    response = Thread(target=self.handleRequest, args=(connection, address))
                    response.start()
                    self.threads.append(response)
                elif readyInput == stdin:
                    isRunning = False
        self.stop()

    # Gracefully stops the server
    def stop(self):
        self.tcpSocket.close()
        for response in self.threads:
            response.join()

    # retrives a value from the key value server based on a give key
    def get(self, key):
        self.keyValLock.acquire()
        value = self.keyVal[key]
        print("Sent " + key + " : " + value + " " + str(time.time() * 1000))
        self.keyValLock.release()
        return value

    # creates a new key-value pair in the key-value store
    def put(self, key, value):
        self.keyValLock.acquire()
        self.keyVal[key] = value
        print("Added " + key + " : " + value + " " + str(time.time() * 1000))
        testValue = self.keyVal[key]
        self.keyValLock.release()
        return testValue == value

    # deletes a key from the key values store based on a given key
    def delete(self, key):
        self.keyValLock.acquire()
        self.keyVal.pop('key', None)
        print("Deleted " + key + " " + str(time.time() * 1000))
        self.keyValLock.release()
        return True


def main():
    # Get all but the first argument
    arguments = argv[1:]
    tcpPort = 0
    if len(arguments) != 2:
        print("server <tcpPort>")
        tcpPort = 5557
    else:
        tcpPort = int(arguments[0])

    keyValServer = KeyValServer(tcpPort)

    print("Press Ctrl-c to end server")

    try:
        keyValServer.run()
    except KeyboardInterrupt:
        print("\nClosing Server Have A Nice Day")


if __name__ == '__main__':
    main()
