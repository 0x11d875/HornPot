import datetime
import select
import socket
import sqlite3
import time

ip = "127.0.0.1"
portList = [
    22, # ssh
    23, # telent
]


#Old used ports
#1080, 33443, 33444, 52285, 5555, 5631, 63358, 63544, 81, 1222, 1338, 1475, 1582, 1730, 21389, 21390, 21391, 21392,
#21393, 33445, 33446, 33447, 34592, 4300, 45380, 45381, 45382, 45383, 45384, 45386, 45387, 45388, 45389, 45390,
#45391, 45392, 45393, 45394, 45395, 45396, 45397, 45398, 45399, 45400, 5338, 10097, 12294, 2145, 2323, 2466, 26549,
#26556, 3627, 3912, 57879, 65234, 8080, 9275, 3753, 80, 7071, 445, 443, 123, 8900, 41470, 5901, 5902, 68, 23, 22,
#445, 80, 65531, 58122, 25




class Database:

    def __init__(self):
        self.con = sqlite3.connect('connections.db')
        self.cur = self.con.cursor()

        self.create_tables()

    def __del__(self):
        self.con.close()

    def create_tables(self):
        connections_table = """CREATE TABLE IF NOT EXISTS CREATE TABLE "connection" (
                            "id"	INTEGER, AUTOINCREMENT
                            "timestamp"	TEXT,
                            "source port"	TEXT,
                            "source ip"	TEXT,
                            "content"	BLOB
                            );"""

        self.cur.execute(connections_table)


class Logger():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def log(self, msg):
        timstr = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

        f = open("logs/port" + str(self.port) + ".log", 'a')
        f.writelines(timstr + ": " + msg + '\r\n')
        f.close()


class SimpleSocket(object):
    def __init__(self, logger, so=None):
        self.logger = logger
        if so is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = so

        self.ip = ""
        self.port = 0
        self.setBlocking(True)

    def setBlocking(self, setter):
        self.socket.setblocking(setter)

    def recv(self):
        try:
            msg = self.socket.recv(4069)
        except Exception as e:
            self.logger.log(str(e) + "on rec " + self.ip + ":" + str(self.port))
            return None

        return msg

    def send(self, msg):
        try:
            self.logger(str(self.ip) + ":" + str(self.port) + " <- " + str(msg))
            return self.socket.send(msg)
        except Exception as e:
            self.logger.log("fail " + str(e))
            return 0

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass

        try:
            self.socket.close()
        except:
            pass

        self.logger.log("Closed " + str(self.ip) + ":" + str(self.port))
        self.ip = ""
        self.port = 0

    def connect(self, host, port):
        self.socket.connect((host, port))

    def bindListenAndGo(self, ip, port):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ip = ip
        self.port = port
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        # self.logger.log("HornyPot is running on " + str(self.ip) + ":" + str(self.port))

    def accept(self):

        try:
            clientSocket, clientAddress = self.socket.accept()

            newSimpSock = SimpleSocket(self.logger, clientSocket)

            (ip, port) = clientAddress
            newSimpSock.ip = ip
            newSimpSock.port = port
            self.logger.log("Accepted new Client " + str(ip) + ":" + str(port))

            return newSimpSock

        except:
            self.logger.log("Unable to accept")

            return None


class Service():
    def __init__(self, ip, port):

        self.ip = ip
        self.port = port
        self.logger = Logger(ip, port)

        self.serverSo = SimpleSocket(self.logger)
        self.serverSo.bindListenAndGo(ip, port)

        self.allSockets = [self.serverSo.socket]
        self.clientsWeWantToWrite = []
        self.clientsWriteQueue = {}

        self.socketToSimSo = {}

        self.socketToSimSo[self.serverSo.socket] = self.serverSo

    def addSoToList(self, siSocket):
        self.socketToSimSo[siSocket.socket] = siSocket
        self.allSockets.append(siSocket.socket)

    def removeSoFromList(self, siSocket):
        self.socketToSimSo.pop(siSocket.socket)
        self.allSockets.remove(siSocket.socket)

    def socketToSimpleSocket(self, soc):
        try:
            return self.socketToSimSo[soc]
        except:
            return None

    def closeClient(self, siSo):
        self.removeSoFromList(siSo)
        siSo.close()

    def readFromClient(self, siSo):
        msg = siSo.recv()

        if msg is None:
            return 0

        if len(msg) != 0:
            self.logger.log(siSo.ip + ":" + str(siSo.port) + " -> " + str(msg))

        return len(msg)

    def acceptClient(self):

        cliSo = self.serverSo.accept()

        if cliSo is None:
            return

        # cliSo.send(b'\r\n\r\n\r\nWelcome to Microsoft Telnet HornyPot.\r\n\r\nC:\\>')
        self.addSoToList(cliSo)

    def handleReadable(self, so):
        s = self.socketToSimpleSocket(so)
        if s is self.serverSo:
            # here we have to handle a new connection
            self.acceptClient()

        else:
            # here we can read from the sockets.
            le = self.readFromClient(s)

            if le == 0:
                self.closeClient(s)
                # clear writable socket lsit

    def handleWritable(self):
        pass

    def handleExceptional(self, so):
        s = self.socketToSimpleSocket(so)
        self.logger.log("Socket " + str(s) + " is exeptional. So we close it")
        if s == self.serverSo:
            self.logger.log("Socket " + str(s) + " is exeptional. AND IT'S THE SERVER SOCKET")


class HornyPot():
    def __init__(self, services):

        if len(services) == 0:
            print("No services activ. Terminate HornyPot.")
            return

        self.logger = Logger(ip, "Main")

        self.allServices = services
        self.allSockets = []

        for serv in services:
            self.allSockets.append(serv.serverSo.socket)
        self.serverSo = self.allSockets

        self.clientsWeWantToWrite = []

        self.mainLoop()

    def refreshAllSocketList(self):
        self.allSockets = []
        for serv in self.allServices:
            self.allSockets += serv.allSockets

    def socketToService(self, soc):
        for serv in self.allServices:
            simplSo = serv.socketToSimpleSocket(soc)

            if simplSo is not None:
                return serv
        self.logger.log("Unable to find socket")
        return None

    def mainLoop(self):

        print("HornyPot is running")

        while True:
            readable, writable, exeptional = select.select(self.allSockets, self.clientsWeWantToWrite, self.allSockets)

            for s in readable:
                servi = self.socketToService(s)
                servi.handleReadable(s)
                self.refreshAllSocketList()

            for s in writable:
                servi = self.socketToService(s)
                servi.handleWritable(s)
                self.refreshAllSocketList()

            for s in exeptional:
                servi = self.socketToService(s)
                servi.handleExeptional(s)
                self.refreshAllSocketList()


serviceList = []
# portList = set([23])

for port in portList:

    try:
        serv = Service(ip, port)
        serviceList.append(serv)
    except Exception as e:
        print("Port: " + str(port) + str(e))
        pass

serv = HornyPot(serviceList)
