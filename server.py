#!./env/bin/python3

# Imports
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOCK_DGRAM
from socket import SOL_SOCKET
from socket import SO_REUSEADDR
from json import loads
from json import dumps
from threading import Thread
from threading import Lock
from sys import stdin
from sys import argv
from select import select
import time
import grpc
import distributedKeyValStore_pb2
from concurrent import futures

"""
KeyValServer class extends the KeyValStoreServicer class
serverAddress: (string) the local address of the server
tcpPort: (int) the port number for tcp communications
udpPort: (int) the port number for udp communications
rpcPort: (int) the port number for rpc communications
bufferSize: (int) buffer size for sending information
"""
class KeyValServer(distributedKeyValStore_pb2.KeyValStoreServicer):
    def __init__(self, serverAddress, tcpPort, udpPort, bufferSize):
        self.keyVal = {}
        self.keyValLock = Lock()
        self.serverAddress = serverAddress
        self.tcpPort = tcpPort
        self.udpPort = udpPort
        self.bufferSize = bufferSize
        self.backlog = 5
        self.tcpSocket = None
        self.udpSocket = None
        self.threads = []

    # Decode message takes binary data and converts it to a python dictionary
    def decodeMessage(self, binaryData):
        if(type(binaryData) is tuple):
            binaryData = binaryData[0]
        receivedString = binaryData.decode("ascii")
        message = loads(receivedString)
        return message

    # EncodeMessage takes string arugments and converts it to a JSON formatted string
    def encodeMessage(self, command="", key="", value="", error="", success=""):
        dictionary = {}
        dictionary["command"] = command
        dictionary["key"] = key
        dictionary["value"] = value
        dictionary["success"] = success
        dictionary["error"] = error
        message = dumps(dictionary)
        return message

    # OpenSockets opens the sockets for both TCP and UDP
    # and sets self.tcpSocket and self.udpSocket for the server
    def openSockets(self):
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        self.tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.tcpSocket.bind((self.serverAddress, self.tcpPort))
        self.tcpSocket.listen(self.backlog)

        self.udpSocket = socket(AF_INET, SOCK_DGRAM)
        self.udpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.udpSocket.bind((self.serverAddress, self.udpPort))

    # Handles a TCP Request by decoding the incoming message
    # completing the given request and sending an encoded message
    # back to the sender
    def handleTCPRequest(self, connection, address):
        isRunning = True
        while isRunning:
            data = connection.recv(self.bufferSize)
            if not data:
                break
            inMessage = self.decodeMessage(data)
            outMessage = ""
            command = inMessage["command"]
            if(command == "get"):
                key = inMessage["key"]
                value = self.get(key)
                outMessage = self.encodeMessage(key=key, value=value, success=True)
            elif(command == "put"):
                key = inMessage["key"]
                value = inMessage["value"]
                success = self.put(key, value)
                outMessage = self.encodeMessage(key=key, value=value, success=success)
            elif(command == "delete"):
                key = inMessage["key"]
                success = self.delete(key)
                outMessage = self.encodeMessage(key=key, success=success)
            else:
                error = "No command called " + command
                outMessage = self.encodeMessage(success=False, error=error)
            connection.send(outMessage.encode("ascii"))
            isRunning = False
        connection.close()

    # Handles a UDP Request by decoding the incoming message
    # completing the given request and sending an encoded message
    # back to the sender
    def handleUDPRequest(self):
        isRunning = True
        while isRunning:
            data, address = self.udpSocket.recvfrom(self.bufferSize)
            if not data:
                break
            inMessage = self.decodeMessage(data)
            outMessage = ""
            command = inMessage["command"]
            if(command == "get"):
                key = inMessage["key"]
                value = self.get(key)
                outMessage = self.encodeMessage(key=key, value=value, success=True)
            elif(command == "put"):
                key = inMessage["key"]
                value = inMessage["value"]
                success = self.put(key, value)
                outMessage = self.encodeMessage(key=key, value=value, success=success)
            elif(command == "delete"):
                key = inMessage["key"]
                success = self.delete(key)
                outMessage = self.encodeMessage(key=key, success=success)
            else:
                error = "No command called " + command
                outMessage = self.encodeMessage(success=False, error=error)

            self.udpSocket.sendto(outMessage.encode("ascii"), address)
            isRunning = False

    # The main loop for the server delagates handling of all requests
    def run(self):
        self.openSockets()
        inputs = [self.tcpSocket, self.udpSocket, stdin]
        isRunning = True
        while isRunning:
            readyInputs, readyOutputs, readyExcepts = select(inputs, [], [])
            for readyInput in readyInputs:
                if(readyInput == self.tcpSocket):
                    connection, address = self.tcpSocket.accept()
                    response = Thread(target=self.handleTCPRequest, args=(connection, address))
                    response.start()
                    self.threads.append(response)
                elif(readyInput == self.udpSocket):
                    response = Thread(target=self.handleUDPRequest, args=())
                    response.start()
                    self.threads.append(response)
                elif(readyInput == stdin):
                    isRunning = False
        self.stop()

    # Gracefully stops the server
    def stop(self):
        self.tcpSocket.close()
        self.udpSocket.close()
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

    # get command that can be called by a rpc request
    def getrpc(self, request, context):
        value = self.get(request.key)
        return distributedKeyValStore_pb2.GetReply(key=request.key, value=value, success=True)

    # put command that can be called by a rpc request
    def putrpc(self, request, context):
        success = self.put(request.key, request.value)
        return distributedKeyValStore_pb2.PutRequest(key=request.key, value=request.value, success=success)

    # delete command that can be called by a rpc request
    def deleterpc(self, request, context):
        success = self.delete(request.key)
        return distributedKeyValStore_pb2.PutRequest(key=request.key, success=success)


def main():
    # Get all but the first arugment
    arguments = argv[1:]
    if (len(arguments) != 3):
        print("server <tcpPort> <udpPort> <rpcPort>")
    print("Press Ctrl-c to end server")
    ip = "127.0.0.1"
    tcpPort = int(arguments[0])
    udpPort = int(arguments[1])
    rpcPort = int(arguments[2])
    bufferSize = 1024
    keyValServer = KeyValServer(ip, tcpPort, udpPort, bufferSize)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    distributedKeyValStore_pb2.add_KeyValStoreServicer_to_server(keyValServer, server)
    server.add_insecure_port("[::]:" + str(rpcPort))
    server.start()
    try:
        keyValServer.run()
    except KeyboardInterrupt:
        server.stop(0)
        print()
        print("Closing Server Have A Nice Day")

if __name__ == '__main__':
    main()
