#!./env/bin/python3

# Imports
from csv import reader
from sys import argv
from keyValNode import KeyValNode


# KeyValClient
# serverAddress: (string) the address of the server
# port: (int) the port number for communications
class KeyValClient(KeyValNode):
    def __init__(self, serverAddress, port):
        super().__init__(port)
        self.serverAddress = serverAddress

    # sends a get request
    def get(self, key):
        outMessage = self.encodeMessage(command="get", key=key)
        inMessage = self.sendMessage(outMessage, self.serverAddress)
        value = inMessage["value"]
        success = bool(inMessage["success"])

        if success:
            print(str(key), ":", str(value), "retrieved")
        else:
            print(str(key), "not retrieved")

    # sends a put request
    def put(self, key, value):
        outMessage = self.encodeMessage(command="put", key=key, value=value)
        inMessage = self.sendMessage(outMessage, self.serverAddress)
        success = bool(inMessage["success"])

        if success:
            print(str(key), ":", str(value), "added")
        else:
            print(str(key), ":", str(value), "not added")

    # sends a delete request
    def delete(self, key):
        success = False

        outMessage = self.encodeMessage(command="delete", key=key)
        inMessage = self.sendMessage(outMessage, self.serverAddress)
        success = bool(inMessage["success"])

        if success:
            print(str(key) + " removed")
        else:
            print(str(key) + " not removed")


def main():
    arguments = argv[1:]
    serverAddress = ""
    port = 0
    if len(arguments) != 2:
        print("client <serverAddress> <port>")
        serverAddress = "127.0.0.1"
        port = 5557
    else:
        serverAddress = arguments[0]
        port = int(arguments[1])

    testOperationsPath = "data/kvp-operations.csv"

    keyValClient = KeyValClient(serverAddress, port)

    with open(testOperationsPath, newline="\n") as operationsFile:
        operationReader = reader(operationsFile, delimiter=",")
        for operation in operationReader:
            command = operation[0]
            if command == "PUT":
                keyValClient.put(operation[1], operation[2])
            elif command == "GET":
                keyValClient.get(operation[1])
            elif command == "DELETE":
                keyValClient.delete(operation[1])
            else:
                print(command + " is not a valid command")


if __name__ == "__main__":
    main()
