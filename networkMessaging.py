from json import loads
from json import dumps


# Decode message takes binary data and converts it to a python dictionary
def decodeMessage(binaryData):
    if(type(binaryData) is tuple):
        binaryData = binaryData[0]
    receivedString = binaryData.decode("ascii")
    return loads(receivedString)


# EncodeMessage takes string arugments and converts it to a JSON formatted string
def encodeMessage(command="", key="", value="", error="", success=""):
    dictionary = dict()
    dictionary["command"] = command
    dictionary["key"] = key
    dictionary["value"] = value
    dictionary["success"] = success
    dictionary["error"] = error
    return dumps(dictionary)
