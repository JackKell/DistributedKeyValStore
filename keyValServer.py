# Imports
from socket import socket
from socket import gethostname
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOL_SOCKET
from socket import SO_REUSEADDR
from threading import Thread
from threading import Lock
from sys import stdin
from select import select
from time import time
from keyValNode import KeyValNode


# KeyValServer class extends the KeyValStoreServicer class
# serverAddress: (string) the local address of the server
# port: (int) the port number for tcp communications
class KeyValServer(KeyValNode):
    def __init__(self, port):
        KeyValNode.__init__(self, port)
        self.keyVal = {}
        self.keyValLock = Lock()
        self.serverAddress = ""
        self.tcpSocket = None
        self.threads = []
        self.servers = []

    # OpenSockets opens the sockets for both TCP and UDP
    # and sets self.tcpSocket and self.udpSocket for the server
    def openSocket(self):
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        self.tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.tcpSocket.bind((self.serverAddress, self.port))
        self.tcpSocket.listen(self.backlog)

    def twoPhaseCommit(self, inMessage):
        print("Two Phase Commit")
        voteCount = 0
        for server in self.servers:
            if server != gethostname():
                inMessage["isCommit"] = False
                self.sendMessage(inMessage, server)

    # Handles a TCP Request by decoding the incoming message
    # completing the given request and sefr nding an encoded message
    # back to the sender
    def handleRequest(self, connection, address):
        isRunning = True
        while isRunning:
            # Collect all the data from the connection
            data = connection.recv(self.bufferSize)
            # If there is no more data then break the loop
            if not data:
                break

            self.keyValLock.acquire()
            inMessage = self.decodeMessage(data)
            outMessage = ""
            command = inMessage["command"]
            doTwoPhaseCommit = False

            print(inMessage["isCommit"])
            if bool(inMessage["isCommit"]):
                doTwoPhaseCommit = True

            if command == "get":
                key = inMessage["key"]
                value = self.get(key)
                outMessage = self.encodeMessage(key=key, value=value, success=True)
            elif command == "put":
                if doTwoPhaseCommit:
                    self.twoPhaseCommit(inMessage)
                key = inMessage["key"]
                value = inMessage["value"]
                success = self.put(key, value)
                outMessage = self.encodeMessage(key=key, value=value, success=success)
            elif command == "delete":
                if doTwoPhaseCommit:
                    self.twoPhaseCommit(inMessage)
                key = inMessage["key"]
                success = self.delete(key)
                outMessage = self.encodeMessage(key=key, success=success)
            else:
                error = "No command called " + command
                outMessage = self.encodeMessage(success=False, error=error)

            self.keyValLock.release()
            connection.send(outMessage.encode("ascii"))
            isRunning = False
        connection.close()

    # The main loop for the server delegates handling of all requests
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

    # retrieves a value from the key value server based on a give key
    def get(self, key):
        value = self.keyVal[key]
        print("Sent " + key + " : " + value + " " + str(time() * 1000))
        return value

    # creates a new key-value pair in the key-value store
    def put(self, key, value):
        self.keyVal[key] = value
        print("Added " + key + " : " + value + " " + str(time() * 1000))
        testValue = self.keyVal[key]
        return testValue == value

    # deletes a key from the key values store based on a given key
    def delete(self, key):
        self.keyVal.pop('key', None)
        print("Deleted " + key + " " + str(time() * 1000))
        return True
