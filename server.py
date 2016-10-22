#!/usr/bin/env python
import socket
import json


class KeyValServer():
    def __init__(self, serverAddress, port, bufferSize):
        self.keyVal = {}
        self.serverAddress = serverAddress
        self.port = port
        self.bufferSize = bufferSize

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

    def run(self):
        print("Running KeyValServer")
        while True:
            tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcpSocket.bind((self.serverAddress, self.port))
            tcpSocket.listen(1)
            conn, addr = tcpSocket.accept()
            print("Connection address: ", addr)
            while True:
                data = conn.recv(self.bufferSize)
                if not data:
                    break
                inMessage = self.decodeMessage(data)
                outMessage = ""
                print("Received: ", inMessage)
                command = inMessage["command"]
                if(command == "get"):
                    key = inMessage["key"]
                    value = self.get(inMessage["key"])
                    outMessage = self.encodeMessage(key=key, value=value, success=True)
                elif(command == "put"):
                    key = inMessage["key"]
                    value = inMessage["value"]
                    success = self.put(key, value)
                    outMessage = self.encodeMessage(key=key, value=value, success=success)
                elif(command == "delete"):
                    key = inMessage["key"]
                    success = self.delete(key)
                    outMessage = self.encodeMessage(key=key, value=value, success=success)
                else:
                    error = "No command called " + command
                    outMessage = self.encodeMessage(success=False, error=error)
                print("Sent: " + outMessage)
                conn.send(outMessage.encode("ascii"))
            conn.close()

    def get(self, key):
        return self.keyVal[key]

    def put(self, key, value):
        self.keyVal[key] = value
        return self.keyVal[key] == value

    def delete(self, key):
        self.keyVal.pop('key', None)
        return True


def main():
    ip = "127.0.0.1"
    port = 5005
    bufferSize = 1024
    keyValServer = KeyValServer(ip, port, bufferSize)
    keyValServer.run()

main()
