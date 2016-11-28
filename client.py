#!./env/bin/python3

# Imports
from csv import reader
from sys import argv
from keyValClient import KeyValClient

# A function that creates an instance of a KeyValClient
def main():
    arguments = argv[1:]

    if len(arguments) != 2:
        print("client <serverAddress> <port>")
        return

    serverAddress = arguments[0]
    port = int(arguments[1])

    testOperationsPath = "data/kvp-operations.csv"

    # Create an instance of the keyValClient class
    keyValClient = KeyValClient(serverAddress, port)
    keyValClient.timeout = 20

    # Read and send requests to server
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
