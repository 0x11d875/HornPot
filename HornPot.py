import select
import socket

from logger import log, Database
from services.ServiceBase import ServiceBase


class HornPot:

    def __init__(self, services: [ServiceBase]):
        self.services: list[ServiceBase] = services

        self.all_sockets: [socket.socket] = []
        self.clientsWeWantToWrite = []

        self.run()


    def update_all_sockets(self):
            self.all_sockets.clear()
            for service in self.services:
                self.all_sockets += [service.serverSo.socket]
                self.all_sockets += service.get_all_handled_sockets()
                self.clientsWeWantToWrite += service.get_all_needs_write_sockets()

    def socket_to_service(self, soc: socket) -> ServiceBase | None:
        for serv in self.services:
            simplSo = serv.socket_to_session(soc)
            if simplSo is not None:
                return serv
        return None

    def run(self):

        log(f"HornPot is running with {len(self.services)} services.")

        while len(self.services) != 0:

            self.update_all_sockets()

            readable, writable, exeptional = select.select(self.all_sockets, self.clientsWeWantToWrite,
                                                           self.all_sockets, 2)

            for socket in readable:
                service = self.socket_to_service(socket)
                if service is not None:
                    service.handle_readable(socket)

            for socket in writable:
                service = self.socket_to_service(socket)
                if service is not None:
                    service.handle_writable(socket)

            for socket in exeptional:
                service = self.socket_to_service(socket)
                if service is not None:
                    crashed = service.handle_exeptional(socket)
                    if crashed:
                        self.services.remove(service)

        log(f"HornPot terminates, no services (left).")
