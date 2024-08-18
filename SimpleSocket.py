import socket

from logger import log


class SimpleSocket:
    # TODO: real IPvAddress type instead of str
    def __init__(self, addr: (str, int), listen: bool = False):
        self.addr = addr

        if listen:
            if socket.has_dualstack_ipv6():
                self.socket = socket.create_server(addr, family=socket.AF_INET6, reuse_port=True, dualstack_ipv6=True)
            else:
                self.socket = socket.create_server(addr, family=socket.AF_INET, reuse_port=True)

            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.ip, self.port))
            self.socket.listen(1)
        else:
            try:
                self.socket = socket.create_connection(self.addr, source_address=None)
            except e:
                pass

    def __del__(self):
        self.close()

    def set_blocking(self, setter: bool):
        self.socket.setblocking(setter)

    def recv(self):
        try:
            msg = self.socket.recv(4069)
        except OSError as e:
            #log(str(e) + "on rec " + self.ip + ":" + str(self.port))
            return None

        return msg

    def send(self, msg):
        try:
            #log(str(self.ip) + ":" + str(self.port) + " <- " + str(msg))
            return self.socket.send(msg)
        except OSError as e:
            #log("fail " + str(e))
            return 0

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        try:
            self.socket.close()
        except OSError:
            pass

        #log("Closed " + str(self.ip) + ":" + str(self.port))
        self.addr = (" ", 0)

    def accept(self):
        try:
            clientSocket, clientAddress = self.socket.accept()

            newSimpSock = SimpleSocket(clientSocket)

            (ip, port) = clientAddress
            newSimpSock.ip = ip
            newSimpSock.port = port
            #("Accepted new Client " + str(ip) + ":" + str(port))

            return newSimpSock

        except:
            # self.logger.log("Unable to accept")
            return None
