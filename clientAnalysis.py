#!./env/bin/python3
# Imports
from csv import reader
import csv
from sys import argv
from keyValClient import KeyValClient
from time import time

# A function that creates an instance of a KeyValClient
def main():
    arguments = argv[1:]

    if len(arguments) != 2:
        print("client <serverAddress> <port>")
        return

    serverAddress = arguments[0]
    port = int(arguments[1])

    testOperationsPath = "data/kvp-operations.csv"

    keyValClient = KeyValClient(serverAddress, port)

    putcsv = open("output/put.csv", "w")
    getcsv = open("output/put.csv", "w")
    deletecsv = open("output/put.csv", "w")

    putwriter = csv.writer(putcsv)
    getwriter = csv.writer(getcsv)
    deletewriter = csv.writer(deletecsv)

    with open(testOperationsPath, newline="\n") as operationsFile:
        operationReader = reader(operationsFile, delimiter=",")
        for operation in operationReader:
            command = operation[0]
            if command == "PUT":
                start = time() * 1000
                keyValClient.put(operation[1], operation[2])
                end = time() * 1000
                putwriter.writerow([end - start])
            elif command == "GET":
                start = time() * 1000
                keyValClient.get(operation[1])
                end = time() * 1000
                getwriter.writerow([end - start])
            elif command == "DELETE":
                start = time() * 1000
                keyValClient.delete(operation[1])
                end = time() * 1000
                deletewriter.writerow([end - start])
            else:
                print(command + " is not a valid command")

    putcsv.close()
    getcsv.close()
    deletecsv.close()


if __name__ == "__main__":
    main()
