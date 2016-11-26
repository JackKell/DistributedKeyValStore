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
from time import time


# KeyValServer
# port: (int) the port number for tcp communications
class KeyValServer(KeyValNode):
    def __init__(self, port):
        KeyValNode.__init__(self, port)
        self.keyVal = dict()
        self.__keyValLock = Lock()
        self.serverAddress = ""
        self.tcpSocket = None
        self.serverSocket = None
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
        self.proposalTimeout = 1

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
                proposerCommands = ["promise", "accepted", "committed"]
                acceptorCommands = ["prepare", "accept"]
                learnerCommands = ["commit"]

                if command in sessionCommands:
                    self.sessions.put((connection, address, request))
                elif command in proposerCommands:
                    # send to proposer queue
                    self.proposerJobs.put((connection, address, request))
                elif command in acceptorCommands:
                    # send to acceptor queue
                    self.acceptorJobs.put((connection, address, request))
                elif command in learnerCommands:
                    # send to learner queue
                    self.learnerJobs.put((connection, address, request))
                else:
                    print("handler: invalid command", command)
                self.requests.task_done()

    def __proposer(self):
        def __sendPrepare(clock, address):
            print("\tsending prepare message to", address)
            prepareMessage = self.encodeMessage(command="prepare", clock=clock)
            tempSocket = socket(AF_INET, SOCK_STREAM)
            tempSocket.connect((address, self.port))
            tempSocket.settimeout(self.timeout)
            tempSocket.send(prepareMessage.encode("ascii"))

        def __sendAccept(clock, value, address):
            print("\tsending accept message to", address)
            acceptMessage = self.encodeMessage(command="accept", value=value, clock=clock)
            tempSocket = socket(AF_INET, SOCK_STREAM)
            tempSocket.connect((address, self.port))
            tempSocket.settimeout(self.timeout)
            tempSocket.send(acceptMessage.encode("ascii"))

        def __sendCommit(clock, value, address):
            print("\tsending commit message to", address)
            acceptMessage = self.encodeMessage(command="commit", value=value, clock=clock)
            tempSocket = socket(AF_INET, SOCK_STREAM)
            tempSocket.connect((address, self.port))
            tempSocket.settimeout(self.timeout)
            tempSocket.send(acceptMessage.encode("ascii"))

        promises = []
        accepteds = []
        committeds = []
        sentPrepares = False
        sentAccepts = False
        sentCommits = False
        needJob = True
        reachedPromiseQuorum = False
        reachedAcceptedQuorum = False
        clientConnection = None
        clientAddress = None
        clientRequest = None
        clock = 0
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
                    committeds = []
                    sentPrepares = False
                    sentCommits = False
                    sentAccepts = False
                    needJob = False
                    reachedPromiseQuorum = False
                    reachedAcceptedQuorum = False
                    clientConnection, clientAddress, clientRequest = self.sessions.get()
                    acceptedValue = clientRequest
                    clock += 1
                    print("proposer: clock", clock)
            else:
                # put promises and accepted messages into the proposer job queue
                if not self.proposerJobs.empty():
                    serverConnection, serverAddress, serverRequest = self.proposerJobs.get()
                    command = serverRequest["command"]
                    if command == "promise":
                        promises.append((serverConnection, serverAddress, serverRequest))
                    elif command == "accepted":
                        accepteds.append((serverConnection, serverAddress, serverRequest))
                    elif command == "committed":
                        committeds.append((serverConnection, serverAddress, serverRequest))
                    self.proposerJobs.task_done()

                # 2.) Broadcasts Prepare(n) to all servers
                if not sentPrepares:
                    print("proposer: broadcast prepare messages")
                    for serverAddress in self.servers:
                        __sendPrepare(clock, serverAddress)
                    sentPrepares = True

                # 4.) When responses received from majority
                #     If any acceptedValues returned, replace value with acceptedValue for highest acceptedProposal
                if not reachedPromiseQuorum:
                    quorumSize = len(self.servers)
                    if len(promises) >= (quorumSize // 2 + 1):
                        reachedPromiseQuorum = True
                        # greatestClock = clock
                        # for index in range(0, len(promises)):
                        #     currentConnection, currentAddress, currentValue = promises[index]
                        #     currentClock = currentValue["clock"]
                        #     if currentClock > greatestClock:
                        #         greatestValue = currentValue
                        #         greatestClock = currentClock
                        # acceptedValue = greatestValue

                # 5.) Broadcast Accept(n, value) to all servers
                if not sentAccepts and reachedPromiseQuorum:
                    print("proposer: broadcast accept messages")
                    for serverAddress in self.servers:
                        __sendAccept(clock, acceptedValue, serverAddress)
                    sentAccepts = True

                # 7.) When responses received from majority of accepted messages:
                #     - Any rejections result > n go to(step 1) (abort)
                #     - Other wise value is chosen
                if not reachedAcceptedQuorum:
                    quorumSize = len(self.servers)
                    if len(accepteds) >= (quorumSize // 2 + 1):
                        reachedAcceptedQuorum = True

                if not sentCommits and reachedAcceptedQuorum:
                    print("proposer: send commit to the learners")
                    sentCommits = True
                    for accepted in accepteds:
                        learnerAddress = accepted[1][0]
                        __sendCommit(clock, acceptedValue, learnerAddress)

                if sentCommits:
                    quorumSize = len(self.servers)
                    if len(committeds) >= (quorumSize // 2):
                        print(committeds)
                        commmitedRequest = committeds[0][2]
                        outmessage = self.encodeMessage(command="reply",
                                                        key=commmitedRequest["key"],
                                                        value=commmitedRequest["value"],
                                                        success=commmitedRequest["success"],
                                                        clock=commmitedRequest["clock"])
                        clientConnection.send(outmessage.encode("ascii"))
                        needJob = True

    def __acceptor(self):
        def __sendPromise(clock, address):
            print("\tsending promise message to", address)
            promiseMessage = self.encodeMessage(command="promise", clock=clock)
            tempSocket = socket(AF_INET, SOCK_STREAM)
            tempSocket.connect((address, self.port))
            tempSocket.settimeout(self.timeout)
            tempSocket.send(promiseMessage.encode("ascii"))

        def __sendAccepted(address):
            print("\tsending accepted message to", address)
            acceptedMessage = self.encodeMessage(command="accepted", clock=clock)
            tempSocket = socket(AF_INET, SOCK_STREAM)
            tempSocket.connect((address, self.port))
            tempSocket.settimeout(self.timeout)
            tempSocket.send(acceptedMessage.encode("ascii"))

        minProposal = -1
        acceptedValue = None

        while not self.stopEvent.is_set():
            if not self.acceptorJobs.empty():
                connection, address, request = self.acceptorJobs.get()
                command = request["command"]
                clock = request["clock"]
                proposerAddress = address[0]
                print("acceptor: received", command, "message from", proposerAddress)
                if command == "prepare":
                    print("\tclock:", clock, "minProposal:", minProposal)
                    if clock > minProposal:
                        minProposal = clock
                        __sendPromise(clock, proposerAddress)
                    else:
                        print("\tignoring", request)
                elif command == "accept":
                    print("\tclock:", clock, "minProposal:", minProposal)
                    if clock >= minProposal:
                        __sendAccepted(proposerAddress)
                    else:
                        print("\tignoring", request)
                else:
                    print("\treceived invalid command,", command)
                self.acceptorJobs.task_done()

    def __learner(self):
        def __sendCommitted(clock, address, key, value, success):
            print("\tsending committed message to", address)
            committedMessage = self.encodeMessage(command="committed", key=key, value=value, success=success, clock=clock)
            tempSocket = socket(AF_INET, SOCK_STREAM)
            tempSocket.connect((address, self.port))
            tempSocket.settimeout(self.timeout)
            tempSocket.send(committedMessage.encode("ascii"))

        while not self.stopEvent.is_set():
            if not self.learnerJobs.empty():
                connection, address, request = self.learnerJobs.get()
                proposerAddress = address[0]
                clientRequest = request["value"]
                command = clientRequest["command"]
                key = clientRequest["key"]
                value = clientRequest["value"]
                clock = request["clock"]
                success = False
                print("learner: received", command, "message from", address[0])
                if command == "get":
                    value = self.__get(key)
                elif command == "put":
                    success = self.__put(key, value)
                elif command == "delete":
                    success = self.__delete(key)
                else:
                    print("\treceived invalid command,", command)
                    continue
                __sendCommitted(clock, proposerAddress, key, value, success)
                self.learnerJobs.task_done()

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

        self.serverSocket = socket(AF_INET, SOCK_STREAM)

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
        # TODO: make sure to remove this from the project at the end
        # self.requests.put(("connection", "address", {
        #     "command": "put",
        #     "key": 5,
        #     "value": "big"
        # }))

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
        self.__keyValLock.acquire()
        value = self.keyVal[key]
        self.__keyValLock.release()
        print("Got", "(", key, ",", value, ")", time())
        return value

    # creates a new key-value pair in the key-value store
    def __put(self, key, value):
        self.__keyValLock.acquire()
        self.keyVal[key] = value
        testValue = self.keyVal[key]
        self.__keyValLock.release()
        print("Put", "(", key, ",", value, ")", time())
        return testValue == value

    # deletes a key from the key values store based on a given key
    def __delete(self, key):
        self.__keyValLock.acquire()
        self.keyVal.pop('key', None)
        self.__keyValLock.release()
        print("Delete", key, time())
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
