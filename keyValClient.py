# Imports
from keyValNode import KeyValNode


# KeyValClient
# serverAddress: (string) the address of the server
# port: (int) the port number for communications
class KeyValClient(KeyValNode):
    def __init__(self, serverAddress, port):
        KeyValNode.__init__(self, port)
        self.serverAddress = serverAddress

    # sends a get request
    def get(self, key):
        outMessage = self.encodeMessage(command="get", key=key)
        inMessage = self.sendMessage(outMessage, self.serverAddress)
        value = inMessage["value"]
        success = bool(inMessage["success"])
        clock = inMessage["clock"]

        if success:
            print(str(key), ":", str(value), "retrieved", "clock", clock)
        else:
            print(str(key), "not retrieved", "clock", clock)

    # sends a put request
    def put(self, key, value):
        outMessage = self.encodeMessage(command="put", key=key, value=value)
        inMessage = self.sendMessage(outMessage, self.serverAddress)
        success = bool(inMessage["success"])
        clock = inMessage["clock"]

        if success:
            print(str(key), ":", str(value), "added", "clock", clock)
        else:
            print(str(key), ":", str(value), "not added", "clock", clock)

    # sends a delete request
    def delete(self, key):
        success = False

        outMessage = self.encodeMessage(command="delete", key=key)
        inMessage = self.sendMessage(outMessage, self.serverAddress)
        success = bool(inMessage["success"])
        clock = inMessage["clock"]

        if success:
            print(str(key), " removed", "clock", clock)
        else:
            print(str(key), " not removed", "clock", clock)
