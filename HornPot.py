import select
import socket
from logger import log
from services.Service import Service


class HornPot:

    def __init__(self, services: [Service]):
        self.services: list[Service] = services

        self.all_sockets: [socket.socket] = []
        self.write_sockets: list = []

        self.run()

    def update_all_sockets(self):
        self.all_sockets.clear()
        self.write_sockets.clear()
        for service in self.services:
            service.check_quota()
            self.all_sockets += [service.server]
            self.all_sockets += service.get_all_handled_sockets()
            self.write_sockets += service.get_all_needs_write_sockets()

    def socket_to_service(self, s: socket) -> Service | None:
        for service in self.services:
            server_socket = service.socket_to_session(s)
            if server_socket is not None:
                return service
        return None

    def run(self):

        log(f"HornPot is running with {len(self.services)} services.")

        while len(self.services) != 0:

            self.update_all_sockets()

            readable, writable, exceptions = select.select(self.all_sockets, self.write_sockets,
                                                           self.all_sockets, 10)

            for readable_socket in readable:
                service = self.socket_to_service(readable_socket)
                if service is not None:
                    service.handle_readable(readable_socket)

            for writable_socket in writable:
                service = self.socket_to_service(writable_socket)
                if service is not None:
                    service.handle_writable(writable_socket)

            for exceptional_socket in exceptions:
                service = self.socket_to_service(exceptional_socket)
                if service is not None:
                    crashed = service.handle_exceptions(exceptional_socket)
                    if crashed:
                        self.services.remove(service)

        log(f"HornPot terminates, no services (left).")
