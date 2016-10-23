#!/usr/bin/env python
import socket
import json
import threading
import sys
import select


class KeyValServer():
    def __init__(self, serverAddress, tcpPort, udpPort, bufferSize):
        self.keyVal = {}
        self.keyValLock = threading.Lock()
        self.serverAddress = serverAddress
        self.tcpPort = tcpPort
        self.udpPort = udpPort
        self.bufferSize = bufferSize
        self.backlog = 5
        self.tcpSocket = None
        self.udpSocket = None
        self.threads = []

    def decodeMessage(self, binaryData):
        receivedString = binaryData.decode("ascii")
        message = json.loads(receivedString)
        return message

    def encodeMessage(self, command="", key="", value="", error="", success=""):
        dictionary = {}
        dictionary["command"] = command
        dictionary["key"] = key
        dictionary["value"] = value
        dictionary["success"] = success
        dictionary["error"] = error
        message = json.dumps(dictionary)
        return message

    def openSockets(self):
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpSocket.bind((self.serverAddress, self.tcpPort))
        self.tcpSocket.listen(self.backlog)

        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def handleRequest(self, protocol):
        while True:
            data = None
            connection = None
            address = None
            if(protocol == "TCP"):
                connection, address = self.tcpSocket.accept()
                data = connection.recv(self.bufferSize)
            elif(protocol == "UDP"):
                data, address = self.udpSocket.recvfrom(self.bufferSize)
                print(data)
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

            if(protocol == "TCP"):
                connection.send(outMessage.encode("ascii"))
            elif(protocol == "UDP"):
                self.udpSocket.sendto(outMessage.encode("ascii"), (address, self.udpPort))

        if(protocol == "TCP"):
            connection.close()

    def run(self):
        self.openSockets()
        inputs = [self.tcpSocket, self.udpSocket, sys.stdin]
        isRunning = True
        while isRunning:
            readyInputs, readyOutputs, readyExcepts = select.select(inputs, [], [])
            for readyInput in readyInputs:
                if(readyInput == self.tcpSocket):
                    # connection, address = self.tcpSocket.accept()
                    protocol = "TCP"
                    response = threading.Thread(target=self.handleRequest, args=(protocol))
                    response.start()
                    self.threads.append(response)
                elif(readyInput == self.udpSocket):
                    protocol = "UDP"
                    response = threading.Thread(target=self.handleRequest, args=(protocol))
                    response.start()
                    self.threads.append(response)
                elif(readyInput == sys.stdin):
                    isRunning = False

        self.tcpSocket.close()
        self.udpSocket.close()
        for response in self.threads:
            response.join()

    def get(self, key):
        self.keyValLock.acquire()
        value = self.keyVal[key]
        self.keyValLock.release()
        return value

    def put(self, key, value):
        self.keyValLock.acquire()
        self.keyVal[key] = value
        testValue = self.keyVal[key]
        self.keyValLock.release()
        return testValue == value

    def delete(self, key):
        self.keyValLock.acquire()
        self.keyVal.pop('key', None)
        self.keyValLock.release()
        return True


def main():
    ip = "127.0.0.1"
    tcpPort = 5005
    udpPort = 5006
    bufferSize = 1024
    keyValServer = KeyValServer(ip, tcpPort, udpPort, bufferSize)
    keyValServer.run()

main()
