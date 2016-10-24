#!./env/bin/python3

# Imports
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOCK_DGRAM
from json import loads
from json import dumps
from csv import reader
import grpc
import distributedKeyValStore_pb2
from sys import argv

"""
KeyValClient
serverAddress: (string) the address of the server
port: (int) the port number for communications
bufferSize: (int) buffer size for sending information
stub: the grpc stub object
"""
class KeyValClient():
    def __init__(self, serverAddress, port, protocol, bufferSize, stub):
        self.keyVal = {}
        self.serverAddress = serverAddress
        self.port = port
        self.protocol = protocol
        self.bufferSize = bufferSize
        self.stub = stub

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

    # sends a message to the server over the choosen transmission method
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
        else:
            print(self.protocol + " is not a valid protcol")
        return data

    # sends a get request
    def get(self, key):
        value = ""
        success = False
        if(self.protocol == "RPC"):
            response = self.stub.getrpc(distributedKeyValStore_pb2.GetRequest(key=key))
            value = response.value
            success = response.success
        else:
            outMessage = self.encodeMessage(command="get", key=key)
            inMessage = self.decodeMessage(self.send(outMessage))
            value = inMessage["value"]
            success = bool(inMessage["success"])
        if(success):
            print(str(key) + ": " + str(value) + " retrived")
        else:
            print(str(key) + " not retrived")

    # sends a put request
    def put(self, key, value):
        success = False
        if(self.protocol == "RPC"):
            response = self.stub.putrpc(distributedKeyValStore_pb2.PutRequest(key=key, value=value))
            success = response.success
        else:
            outMessage = self.encodeMessage(command="put", key=key, value=value)
            inMessage = self.decodeMessage(self.send(outMessage))
            success = bool(inMessage["success"])
        if(success):
            print(str(key) + ": " + str(value) + " added")
        else:
            print(str(key) + ": " + str(value) + " not added")

    # sends a delete request
    def delete(self, key):
        success = False
        if(self.protocol == "RPC"):
            response = self.stub.deleterpc(distributedKeyValStore_pb2.DeleteRequest(key=key))
            success = response.success
        else:
            outMessage = self.encodeMessage(command="delete", key=key)
            inMessage = self.decodeMessage(self.send(outMessage))
            success = bool(inMessage["success"])
        if(success):
            print(str(key) + " removed")
        else:
            print(str(key) + " not removed")


def main():
    arguments = argv[1:]
    if (len(arguments) != 3):
        print("client <serverAddress> <port> <transmissionMethod>")
        print("<transmissionMethod> must equal:")
        print(" - 'RPC'")
        print(" - 'UDP'")
        print(" - 'TCP'")

    ip = arguments[0]
    port = int(arguments[1])
    protocol = arguments[2].upper()

    bufferSize = 1024
    testOperationsPath = "kvp-operations.csv"

    channel = grpc.insecure_channel(ip + ":" + str(port))
    stub = distributedKeyValStore_pb2.KeyValStoreStub(channel)

    keyValClient = KeyValClient(ip, port, protocol, bufferSize, stub)

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
