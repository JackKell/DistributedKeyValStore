#!./env/bin/python3

# Imports
from sys import argv
from keyValServer import KeyValServer


def main():
    # Get all but the first argument
    arguments = argv[1:]
    tcpPort = 0
    if len(arguments) != 1:
        print("server <tcpPort>")
        tcpPort = 5557
    else:
        tcpPort = int(arguments[0])

    keyValServer = KeyValServer(tcpPort)
    keyValServer.servers = ["n03", "n04", "n05", "n06", "n07"]

    print("Press Ctrl-c to end server")

    try:
        keyValServer.run()
    except KeyboardInterrupt:
        print("\nClosing Server Have A Nice Day")


if __name__ == '__main__':
    main()
