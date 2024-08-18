import socket

class SimpleSocket(object):
    def __init__(self, addr: (str, int), listen: bool = False, so = None):
        if so is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = so

        self.ip = ""
        self.port = 0

        if addr is not None:
            self.ip = addr[0]
            self.port = addr[1]

        self.setBlocking(True)

    def setBlocking(self, setter):
        self.socket.setblocking(setter)

    def recv(self):
        try:
            msg = self.socket.recv(4069)
        except Exception as e:
            return None

        return msg

    def send(self, msg):
        try:
            return self.socket.send(msg)
        except Exception as e:
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


        self.ip = ""
        self.port = 0

    def connect(self, host, port):
        self.socket.connect((host, port))

    def bind_listen_and_go(self, ip, port):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ip = ip
        self.port = port
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        # self.logger.log("HornyPot is running on " + str(self.ip) + ":" + str(self.port))

    def accept(self):

        try:
            clientSocket, clientAddress = self.socket.accept()

            newSimpSock = SimpleSocket(None, False, clientSocket)

            (ip, port) = clientAddress
            newSimpSock.ip = ip
            newSimpSock.port = port

            return newSimpSock

        except:
            return None

