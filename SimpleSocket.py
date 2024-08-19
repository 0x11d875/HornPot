import socket
from collections.abc import Buffer

from logger import log


class ServerSocket:
    # TODO: real IPvAddress type instead of str
    def __init__(self, addr: (str, int)):
        self.addr = addr

        # Should always be true on linux systems
        if socket.has_dualstack_ipv6():
            self.socket = socket.create_server(addr, family=socket.AF_INET6, backlog=1, reuse_port=True,
                                               dualstack_ipv6=True)
        else:
            self.socket = socket.create_server(addr, family=socket.AF_INET, backlog=1, reuse_port=True)

        self.set_blocking(False)

    def __del__(self):
        self.close()

    def set_blocking(self, setter: bool):
        self.socket.setblocking(setter)

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        try:
            self.socket.close()
        except OSError:
            pass

        # log("Closed " + str(self.ip) + ":" + str(self.port))
        self.addr = (" ", 0)

    def accept(self):
        try:
            client_socket, client_address = self.socket.accept()

            new_socket = ClientSocket(client_address, client_socket)

            # ("Accepted new Client " + str(ip) + ":" + str(port))

            return new_socket

        except OSError:
            # self.logger.log("Unable to accept")
            return None


class ClientSocket:
    # TODO: real IPvAddress type instead of str
    def __init__(self, addr: (str, int), other_socket=None):
        self.addr = addr

        if other_socket is None:
            try:
                self.socket = socket.create_connection(self.addr, source_address=None)
            except OSError:
                pass
        else:
            self.socket = other_socket

        self.set_blocking(False)

    def __del__(self):
        self.close()

    def set_blocking(self, setter: bool):
        self.socket.setblocking(setter)

    def recv(self):
        try:
            msg = self.socket.recv(4069)
        except OSError as e:
            # log(str(e) + "on rec " + self.ip + ":" + str(self.port))
            return None

        return msg

    def send(self, msg: Buffer):
        try:
            # log(str(self.ip) + ":" + str(self.port) + " <- " + str(msg))
            return self.socket.send(msg)
        except OSError as e:
            # log("fail " + str(e))
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

        # log("Closed " + str(self.ip) + ":" + str(self.port))
        self.addr = (" ", 0)