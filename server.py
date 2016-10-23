#!/usr/bin/env python
import socket
import json
import threading
import sys
import select


class KeyValServer():
    def __init__(self, serverAddress, port, bufferSize):
        self.keyVal = {}
        self.keyValLock = threading.Lock()
        self.serverAddress = serverAddress
        self.port = port
        self.bufferSize = bufferSize
        self.backlog = 5
        self.server = None
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

    def openSocket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.serverAddress, self.port))
        self.server.listen(1)

    def handleRequest(self, connection, address):
        while True:
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
        connection.close()

    def run(self):
        self.openSocket()
        inputs = [self.server, sys.stdin]
        isRunning = True
        while isRunning:
            readyInputs, readyOutputs, readyExcepts = select.select(inputs, [], [])
            for readyInput in readyInputs:
                if(readyInput == self.server):
                    connection, address = self.server.accept()
                    response = threading.Thread(target=self.handleRequest, args=(connection, address))
                    response.start()
                    self.threads.append(response)
                elif(readyInput == sys.stdin):
                    junk = sys.stdin.readline()
                    isRunning = False

        self.server.close()
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
    port = 5005
    bufferSize = 1024
    keyValServer = KeyValServer(ip, port, bufferSize)
    keyValServer.run()

main()
