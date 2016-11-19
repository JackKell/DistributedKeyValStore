# Imports
from socket import socket
from socket import gethostname
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOL_SOCKET
from socket import SO_REUSEADDR
from threading import Lock
from sys import stdin
from select import select
from time import time
from keyValNode import KeyValNode
from queue import Queue
from threading import Thread
from threading import current_thread
from threading import Event
from time import sleep


# KeyValServer
# port: (int) the port number for tcp communications
class KeyValServer(KeyValNode):
    def __init__(self, port):
        KeyValNode.__init__(self, port)
        self.keyVal = dict()
        self.keyValLock = Lock()
        self.serverAddress = ""
        self.tcpSocket = None
        self.servers = list()
        self.connectionHandlers = list()
        self.requestHandlers = list()
        self.stopEvent = Event()
        self.proposer = None
        self.sessions = Queue()
        self.proposerJobs = Queue()
        self.acceptor = None
        self.acceptorJobs = Queue()
        self.learner = None
        self.learnerJobs = Queue()
        self.connections = Queue()
        self.requests = Queue()
        self.numberOfConnectionHandlers = 10
        self.numberOfRequestHandlers = 10
        self.clock = 0

    """
    def handleRequest(self, connection, address):
        isRunning = True
        while isRunning:
            # Collect all the data from the connection
            data = connection.recv(self.bufferSize)
            # If there is no more data then break the loop
            if not data:
                break

            self.keyValLock.acquire()
            inMessage = self.decodeMessage(data)
            outMessage = ""
            command = inMessage["command"]
            doTwoPhaseCommit = False

            print(inMessage["isCommit"])
            if bool(inMessage["isCommit"]):
                doTwoPhaseCommit = True

            if command == "get":
                key = inMessage["key"]
                value = self.get(key)
                outMessage = self.encodeMessage(key=key, value=value, success=True)
            elif command == "put":
                if doTwoPhaseCommit:
                    self.twoPhaseCommit(inMessage)
                key = inMessage["key"]
                value = inMessage["value"]
                success = self.put(key, value)
                outMessage = self.encodeMessage(key=key, value=value, success=success)
            elif command == "delete":
                if doTwoPhaseCommit:
                    self.twoPhaseCommit(inMessage)
                key = inMessage["key"]
                success = self.delete(key)
                outMessage = self.encodeMessage(key=key, success=success)
            else:
                error = "No command called " + command
                outMessage = self.encodeMessage(success=False, error=error)

            self.keyValLock.release()
            connection.send(outMessage.encode("ascii"))
            isRunning = False
        connection.close()
    """

    def __connectionHandler(self):
        while not self.stopEvent.is_set():
            if not self.connections.empty():
                connection, address = self.connections.get()
                data = connection.recv(self.bufferSize)
                request = self.decodeMessage(data)
                self.requests.put((connection, address, request))
                self.connections.task_done()

    def __requestHandler(self):
        while not self.stopEvent.is_set():
            if not self.requests.empty():
                connection, address, request = self.requests.get()
                command = request["command"]
                print(command)

                sessionCommands = ["get", "put", "delete"]
                proposerCommands = ["promise", "accepted"]
                acceptorCommands = ["prepare", "accept"]
                learnerCommands = ["accepted"]
                if command in sessionCommands:
                    print("sent", command, "job to session queue")
                    self.clock += 1
                    self.sessions.put((connection, address, request, self.clock))
                if command in proposerCommands:
                    # send to proposer queue
                    print("sent", command, "job to proposer")
                    self.proposerJobs.put((connection, address, request))
                if command in acceptorCommands:
                    # send to acceptor queue
                    print("sent", command, "job to acceprot")
                    self.acceptorJobs.put((connection, address, request))
                if command in learnerCommands:
                    # send to learner queue
                    print("sent", command, "job to learner")
                    self.learnerJobs.put((connection, address, request))
                self.requests.task_done()

    def __proposer(self):
        promises = []
        accepteds = []
        sentPrepares = False
        needJob = True
        reachedQuorum = False
        clientConnection = None
        clientAddress = None
        clientRequest = None
        clock = None

        while not self.stopEvent.is_set():
            # if need job, get job
            if needJob == True:
                if not self.sessions.empty():
                    promises = []
                    accepteds = []
                    sentPrepares = False
                    needJob = False
                    reachedQuorum = False
                    clientConnection, clientAddress, clientRequest, clock = self.sessions.get()
                    print("Reached need job stuff")
            else:
                if not sentPrepares:
                    # Send prepares
                    print("sending prepare messages")
                    prepareMessage = self.encodeMessage(command="prepare", clock=clock)
                    for server in self.servers:
                        tcpSocket = socket(AF_INET, SOCK_STREAM)
                        tcpSocket.connect((server, self.port))
                        tcpSocket.settimeout(self.timeout)
                        tcpSocket.send(prepareMessage.encode("ascii"))
                    sentPrepares = True
                if not self.proposerJobs.empty():
                    serverConnection, serverAddress, serverRequest = self.proposerJobs.get()
                    command = serverRequest["command"]
                    if command == "promise":
                        promises.append((serverConnection, serverAddress, serverRequest))
                    elif command == "accepted":
                        accepteds.append((serverConnection, serverAddress, serverRequest))
                    if not reachedQuorum:
                        if (len(promises) / len(self.servers)) > 0.5:
                            # TODO: fix this part
                            highestPromise = promises[0]
                            for index in range:
                                pass

            # else, do we have quorum

            # if we have a quorum - senda accepts


    def __acceptor(self):
        while not self.stopEvent.is_set():
            sleep(1)

    def __learner(self):
        while not self.stopEvent.is_set():
            sleep(1)

    def __startRequestHandlers(self):
        for i in range(0, self.numberOfRequestHandlers):
            requestHandlerThread = Thread(target=self.__requestHandler)
            requestHandlerThread.name = "requestHandler-" + str(i + 1)
            requestHandlerThread.start()
            self.requestHandlers.append(requestHandlerThread)

    def __startConnectionHandlers(self):
        for i in range(0, self.numberOfConnectionHandlers):
            connectionHandlerThread = Thread(target=self.__connectionHandler)
            connectionHandlerThread.name = "connectionHandler-" + str(i + 1)
            connectionHandlerThread.start()
            self.connectionHandlers.append(connectionHandlerThread)

    # OpenSockets opens the sockets for TCP and sets self.tcpSocket value
    def __openSocket(self):
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        self.tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.tcpSocket.bind((self.serverAddress, self.port))
        self.tcpSocket.listen(self.backlog)

    def __initialize(self):
        self.__openSocket()
        self.__startConnectionHandlers()
        self.__startRequestHandlers()
        self.proposer = Thread(target=self.__proposer)
        self.acceptor = Thread(target=self.__acceptor)
        self.learner = Thread(target=self.__learner)
        self.proposer.name = "proposer"
        self.proposer.start()
        self.acceptor.name = "acceptor"
        self.acceptor.start()
        self.learner.name = "learner"
        self.learner.start()

    def start(self):
        self.__initialize()
        self.__run()

    # The main loop for the server
    def __run(self):
        inputs = [self.tcpSocket, stdin]
        while not self.stopEvent.is_set():
            readyInputs, readyOutputs, readyExcepts = select(inputs, [], [])
            for readyInput in readyInputs:
                if readyInput == self.tcpSocket:
                    connection, address = self.tcpSocket.accept()
                    self.connections.put((connection, address))
                elif readyInput == stdin:
                    self.stop()

    # Gracefully stops the server
    def stop(self):
        self.stopEvent.set()

    # retrieves a value from the key value server based on a give key
    def __get(self, key):
        value = self.keyVal[key]
        print("Sent " + key + " : " + value + " " + str(time() * 1000))
        return value

    # creates a new key-value pair in the key-value store
    def __put(self, key, value):
        self.keyVal[key] = value
        print("Added " + key + " : " + value + " " + str(time() * 1000))
        testValue = self.keyVal[key]
        return testValue == value

    # deletes a key from the key values store based on a given key
    def __delete(self, key):
        self.keyVal.pop('key', None)
        print("Deleted " + key + " " + str(time() * 1000))
        return True

"""
    delete this comment
    proposer
        sends
            prepare
            accept
        receives
            promise
            accepted
            rejected

    acceptor
        sends
            promise
            accepted
            rejected
        receives
            prepare
            accept

    learner
        sends
            replys
        receives
            commits

    """
