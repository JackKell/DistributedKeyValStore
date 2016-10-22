#!/usr/bin/env python
import socket
import sys
import json


class KeyValClient():
    def __init__(self, serverAddress, port, protocol, bufferSize):
        self.keyVal = {}
        self.serverAddress = serverAddress
        self.port = port
        self.protocol = protocol
        self.bufferSize = bufferSize

    def decodeMessage(self, binaryData):
        receivedString = binaryData.decode("ascii")
        jsonFormat = receivedString.replace("'", "\"")
        message = json.loads(jsonFormat)
        return message

    def encodeMessage(self, command="", key="", value="", result="", error="", success=""):
        dictionary = {}
        dictionary["command"] = command
        dictionary["key"] = key
        dictionary["value"] = value
        dictionary["success"] = result
        dictionary["error"] = error
        message = str(dictionary).replace("'", "\"")
        return message

    def send(self, message):
        if (self.protocol == "TCP"):
            print("Sent: ", message)
            tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpSocket.connect((self.serverAddress, self.port))
            tcpSocket.send(message.encode("ascii"))
            data = tcpSocket.recv(self.bufferSize)
            tcpSocket.close()
            print("Received: ", data.decode("ascii"))
            return data
        elif (self.protocol == "UDP"):
            print("UDP not implemented")
        elif (self.protocol == "RPC"):
            print("RPC not implemented")
        else:
            print(self.protocol + " is not a valid protcol")

    def get(self, key):
        outMessage = self.encodeMessage(command="get", key=key)
        inMessage = self.decodeMessage(self.send(outMessage))
        return inMessage["value"]

    def put(self, key, value):
        outMessage = self.encodeMessage(command="put", key=key, value=value)
        inMessage = self.decodeMessage(self.send(outMessage))
        if(bool(inMessage["success"])):
            print(str(key) + " was successfully added with value of " + str(value))
        else:
            print(str(key) + " was successfully added with value of " + str(value))

    def delete(self, key):
        outMessage = self.encodeMessage(command="delete", key=key)
        inMessage = self.decodeMessage(self.send(outMessage))
        return inMessage["success"]


def main():
    ip = "127.0.0.1"
    port = 5005
    protocol = "TCP"
    bufferSize = 1024
    message = "I want to travel to another place"

    keyValClient = KeyValClient(ip, port, protocol, bufferSize)
    keyValClient.put("Bob", 26)
    # keyValClient.send(message)

main()
