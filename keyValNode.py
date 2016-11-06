# Imports
from json import loads
from json import dumps
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM


class KeyValNode:
    def __init__(self, port):
        self.port = port
        self.timeout = 5
        self.bufferSize = 1024
        self.backlog = 25

    # Decode message takes binary data and converts it to a python dictionary
    def decodeMessage(self, binaryData):
        if type(binaryData) is tuple:
            binaryData = binaryData[0]
        receivedString = binaryData.decode("ascii")
        return loads(receivedString)

    # EncodeMessage takes string arguments and converts it to a JSON formatted string
    def encodeMessage(self, command="", key="", value="", error="", success=""):
        dictionary = dict()
        dictionary["command"] = command
        dictionary["key"] = key
        dictionary["value"] = value
        dictionary["success"] = success
        dictionary["error"] = error
        return dumps(dictionary)

    # sends a message to the server
    def sendMessage(self, message, destinationAddress):
        tcpSocket = socket(AF_INET, SOCK_STREAM)

        tcpSocket.connect((destinationAddress, self.port))
        tcpSocket.settimeout(self.timeout)
        tcpSocket.send(message.encode("ascii"))
        data = tcpSocket.recv(self.bufferSize)

        data = self.decodeMessage(data)
        tcpSocket.close()
        return data
