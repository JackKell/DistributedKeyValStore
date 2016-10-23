#!/usr/bin/env python
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOCK_DGRAM
from json import loads
from json import dumps
from csv import reader


class KeyValClient():
    def __init__(self, serverAddress, port, protocol, bufferSize):
        self.keyVal = {}
        self.serverAddress = serverAddress
        self.port = port
        self.protocol = protocol
        self.bufferSize = bufferSize

    def decodeMessage(self, binaryData):
        if(type(binaryData) is tuple):
            binaryData = binaryData[0]
        receivedString = binaryData.decode("ascii")
        message = loads(receivedString)
        return message

    def encodeMessage(self, command="", key="", value="", error="", success=""):
        dictionary = {}
        dictionary["command"] = command
        dictionary["key"] = key
        dictionary["value"] = value
        dictionary["success"] = success
        dictionary["error"] = error
        message = dumps(dictionary)
        return message

    def send(self, message):
        data = ""
        if (self.protocol == "TCP"):
            tcpSocket = socket(AF_INET, SOCK_STREAM)
            tcpSocket.connect((self.serverAddress, self.port))
            tcpSocket.send(message.encode("ascii"))
            data = tcpSocket.recv(self.bufferSize)
            tcpSocket.close()
        elif (self.protocol == "UDP"):
            udpSocket = socket(AF_INET, SOCK_DGRAM)
            udpSocket.sendto(message.encode("ascii"), (self.serverAddress, self.port))
            data = udpSocket.recvfrom(self.bufferSize)
            udpSocket.close()
        elif (self.protocol == "RPC"):
            print("RPC not implemented")
        else:
            print(self.protocol + " is not a valid protcol")
        return data

    def get(self, key):
        outMessage = self.encodeMessage(command="get", key=key)
        inMessage = self.decodeMessage(self.send(outMessage))
        if(bool(inMessage["success"])):
            print(str(key) + ": " + str(inMessage["value"]) + " retrived")
        else:
            print(str(key) + " not retrived")

    def put(self, key, value):
        outMessage = self.encodeMessage(command="put", key=key, value=value)
        inMessage = self.decodeMessage(self.send(outMessage))
        if(bool(inMessage["success"])):
            print(str(key) + ": " + str(value) + " added")
        else:
            print(str(key) + ": " + str(value) + " not added")

    def delete(self, key):
        outMessage = self.encodeMessage(command="delete", key=key)
        inMessage = self.decodeMessage(self.send(outMessage))
        if(bool(inMessage["success"])):
            print(str(key) + " removed")
        else:
            print(str(key) + " not removed")


def main():
    ip = "127.0.0.1"
    port = 5005
    protocol = "UDP"
    if(protocol == "TCP"):
        port = 5005
    elif(protocol == "UDP"):
        port = 5006
    bufferSize = 1024
    testOperationsPath = "kvp-operations.csv"

    keyValClient = KeyValClient(ip, port, protocol, bufferSize)

    with open(testOperationsPath, newline="\n") as operationsFile:
        operationReader = reader(operationsFile, delimiter=",")
        for operation in operationReader:
            command = operation[0]
            if(command == "PUT"):
                keyValClient.put(operation[1], operation[2])
            elif(command == "GET"):
                keyValClient.get(operation[1])
            elif(command == "DELETE"):
                keyValClient.delete(operation[1])
            else:
                print(command + " is not a valid command")

if __name__ == '__main__':
    main()
