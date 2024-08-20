import select
import socket
from logger import log
from services.Service import Service


class HornPot:

    def __init__(self, services: [Service]):
        self.services: list[Service] = services

        self.epoll = select.epoll()
        self.registered_fileno = set()
        self.socket_to_service_map = {}

        self.run()

    def epoll_unregister(self, fileno):
        if fileno in self.registered_fileno:
            self.registered_fileno.remove(fileno)
            self.epoll.unregister(fileno)

    def epoll_register(self, fileno, events):
        if fileno not in self.registered_fileno:
            self.registered_fileno.add(fileno)
            self.epoll.register(fileno, events)

    def epoll_clear(self):
        for fileno in self.registered_fileno:
            try:
                self.epoll.unregister(fileno)
            except OSError:
                pass
        self.registered_fileno.clear()


    def update_all_sockets(self):
        self.epoll_clear()
        self.socket_to_service_map.clear()

        for service in self.services:
            service.check_quota()

            self.register_socket(service.server, service)

            want_write = service.get_all_needs_write_sockets()
            for sock in service.get_all_handled_sockets():
                if sock in want_write:
                    self.register_socket(sock, service, writable=True)
                else:
                    self.register_socket(sock, service)

    def get_socket_from_fileno(self, fileno: int) -> socket.socket | None:
        for service in self.services:
            for sock in service.get_all_handled_sockets():
                if sock.fileno() == fileno:
                    return sock
            if service.server.fileno() == fileno:
                return service.server
        return None

    def register_socket(self, sock: socket.socket, service: Service, writable=False):
        events = select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP
        if writable:
            events |= select.EPOLLOUT

        self.epoll_register(sock.fileno(), events)
        self.socket_to_service_map[sock.fileno()] = service

    def socket_to_service(self, fileno: int) -> Service | None:
        return self.socket_to_service_map.get(fileno, None)

    def run(self):

        log(f"HornPot is running with {len(self.services)} services.")

        while len(self.services) != 0:

            self.update_all_sockets()

            events = self.epoll.poll(10)

            for fileno, event in events:
                service = self.socket_to_service(fileno)
                if service is not None:
                    sock = self.get_socket_from_fileno(fileno)
                    if event & select.EPOLLIN:
                        service.handle_readable(sock)
                    if event & select.EPOLLOUT:
                        service.handle_writable(sock)
                    if event & (select.EPOLLERR | select.EPOLLHUP):
                        crashed = service.handle_exceptions(sock)
                        if crashed:
                            self.services.remove(service)

        log(f"HornPot terminates, no services (left).")
