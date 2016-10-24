from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOCK_DGRAM
from json import loads
from json import dumps
from csv import reader
import grpc
import distributedKeyValStore_pb2
import csv
import time

class KeyValClient():
    def __init__(self, serverAddress, port, protocol, bufferSize, stub):
        self.keyVal = {}
        self.serverAddress = serverAddress
        self.port = port
        self.protocol = protocol
        self.bufferSize = bufferSize
        self.stub = stub

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
        else:
            print(self.protocol + " is not a valid protcol")
        return data

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
    ip = "127.0.0.1"
    port = 5005

    protocols = ["TCP", "UDP", "RPC"]
    for protocol in protocols:

        if(protocol == "TCP"):
            port = 5005
        elif(protocol == "UDP"):
            port = 5006
        elif(protocol == "RPC"):
            port = 5007
        else:
            print(protocol + " is not a valid protocol")
            return

        putcsv = open("output/" + protocol.lower() + "put.csv", "w")
        getcsv = open("output/" + protocol.lower() + "get.csv", "w")
        deletecsv = open("output/" + protocol.lower() + "delete.csv", "w")

        putwriter = csv.writer(putcsv)
        getwriter = csv.writer(getcsv)
        deletewriter = csv.writer(deletecsv)

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
                    start = time.time() * 1000
                    keyValClient.put(operation[1], operation[2])
                    end = time.time() * 1000
                    putwriter.writerow([end - start])
                elif(command == "GET"):
                    start = time.time() * 1000
                    keyValClient.get(operation[1])
                    end = time.time() * 1000
                    getwriter.writerow([end - start])
                elif(command == "DELETE"):
                    start = time.time() * 1000
                    keyValClient.delete(operation[1])
                    end = time.time() * 1000
                    deletewriter.writerow([end - start])
                else:
                    print(command + " is not a valid command")

if __name__ == '__main__':
    main()
