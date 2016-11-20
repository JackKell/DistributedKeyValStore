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
        self.__keyValLock = Lock()
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

                sessionCommands = ["get", "put", "delete"]
                proposerCommands = ["promise", "accepted"]
                acceptorCommands = ["prepare", "accept"]
                learnerCommands = ["accepted"]

                if command in sessionCommands:
                    print("sent", command, "job to session queue")
                    self.sessions.put((connection, address, request))
                if command in proposerCommands:
                    # send to proposer queue
                    print("sent", command, "job to proposer")
                    self.proposerJobs.put((connection, address, request))
                if command in acceptorCommands:
                    # send to acceptor queue
                    print("sent", command, "job to acceptor")
                    self.acceptorJobs.put((connection, address, request))
                if command in learnerCommands:
                    # send to learner queue
                    print("sent", command, "job to learner")
                    self.learnerJobs.put((connection, address, request))
                self.requests.task_done()

    def __proposer(self):
        def __sendPrepare(clock, address):
            print("sending prepare messages to", address)
            prepareMessage = self.encodeMessage(command="prepare", clock=clock)
            tempSocket = socket(AF_INET, SOCK_STREAM)
            tempSocket.connect((address, self.port))
            tempSocket.settimeout(self.timeout)
            tempSocket.send(prepareMessage.encode("ascii"))

        def __sendAccept(clock, value, address):
            print("sending accept messages to", address)
            acceptMessage = self.encodeMessage(command="accept", value=value, clock=clock)
            tempSocket = socket(AF_INET, SOCK_STREAM)
            tempSocket.connect((server, self.port))
            tempSocket.settimeout(self.timeout)
            tempSocket.send(acceptMessage.encode("ascii"))

        promises = []
        accepteds = []
        sentPrepares = False
        sentAccepts = False
        needJob = True
        reachedPromiseQuorum = False
        reachedAcceptedQuorum = False
        clientConnection = None
        clientAddress = None
        clientRequest = None
        clock = None
        acceptedClock = None
        acceptedValue = None

        # Proposer
        while not self.stopEvent.is_set():
            # if need job, get job
            if needJob:
                # 1.) Chooses a new proposal number n
                if not self.sessions.empty():
                    promises = []
                    accepteds = []
                    sentPrepares = False
                    needJob = False
                    reachedPromiseQuorum = False
                    reachedAcceptedQuorum = False
                    clientConnection, clientAddress, clientRequest = self.sessions.get()
                    acceptedValue = clientRequest
            else:
                # put promises and accepted messages into the proposer job queue
                if not self.proposerJobs.empty():
                    serverConnection, serverAddress, serverRequest = self.proposerJobs.get()
                    clock = serverRequest["clock"]
                    command = serverRequest["command"]
                    if command == "promise":
                        promises.append((serverConnection, serverAddress, serverRequest))
                    elif command == "accepted":
                        accepteds.append((serverConnection, serverAddress, serverRequest))
                    self.proposerJobs.task_done()

                # 2.) Broadcasts Prepare(n) to all servers
                if not sentPrepares:
                    for server in self.servers:
                        __sendPrepare(clock, server)
                    sentPrepares = True

                # 4.) When responses received from majority
                #     If any acceptedValues returned, replace value with acceptedValue for highest acceptedProposal
                if not reachedPromiseQuorum:
                    quorumSize = len(self.servers)
                    if len(promises) >= (quorumSize // 2 + 1):
                        greatestClock = clock
                        for index in range(0, len(promises)):
                            currentConnection, currentAddress, currentValue = promises[index]
                            currentClock = currentValue["clock"]
                            if currentClock > greatestClock:
                                greatestValue = currentValue
                                greatestClock = currentClock
                        acceptedValue = greatestValue

                # 5.) Broadcast Accept(n, value) to all servers
                if not sentAccepts and reachedPromiseQuorum:
                    for server in self.servers:
                        __sendAccept(acceptedValue, clock, server)
                    sentAccepts = True

                # 7.) When responses received from majority of accepted messages:
                #     - Any rejections result > n go to(step 1) (abort)
                #     - Other wise value is chosen
                if reachedAcceptedQuorum:
                    quorumSize = len(self.servers)
                    if len(promises) >= (quorumSize // 2 + 1):
                        serverConnection, serverAddress, serverRequest = promises[0]
                        for index in range(1, len(promises)):
                            pass

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

    # starts the server and starts all worker threads and main server thread
    def start(self):
        self.__initialize()
        self.__run()

    # Gracefully stops the server
    def stop(self):
        self.stopEvent.set()

"""
    delete this comment
    proposer
        sends
            prepare
            accept
        receives
            promise
            accepted

    acceptor
        sends
            promise
            accepted
        receives
            prepare
            accept

    learner
        sends
            replys
        receives
            commits

    """
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
