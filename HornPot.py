import select
import socket
from logger import log
from services.Service import Service


class HornPot:

    def __init__(self, services: [Service]):
        self.services: list[Service] = services

        self.epoll = select.epoll()
        self.socket_to_service_map = {}

        self.run()

    def epoll_unregister(self, fileno):
        print(f"Unregister {fileno}")
        try:
            self.epoll.unregister(fileno)
        except OSError:
            pass
        self.socket_to_service_map.pop(fileno)

    def epoll_register(self, fileno, events):
        print(f"Register {fileno}")
        self.epoll.register(fileno, events)

    def get_socket_from_fileno(self, fileno: int) -> socket.socket | None:
        for service in self.services:
            for sock in service.get_all_handled_sockets():
                if sock.fileno() == fileno:
                    return sock
            if service.server.fileno() == fileno:
                return service.server
        return None

    def register_socket(self, sock, service: Service, writable=False):
        events = select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP
        if writable:
            events |= select.EPOLLOUT

        if isinstance(sock, socket.socket):
            fileno = sock.fileno()
        else:
            fileno = sock

        self.epoll_register(fileno, events)
        self.socket_to_service_map[fileno] = service

    def run(self):

        log(f"HornPot is running with {len(self.services)} services.")

        for service in self.services:
            self.register_socket(service.server, service, True)

        while len(self.services) != 0:

            for service in self.services:
                killed_sessions = service.check_quota()
                for killed_session in killed_sessions:
                    self.epoll_unregister(killed_session[0].s.fileno())

            events = self.epoll.poll(10)

            for fileno, event in events:
                print(f"Event: {fileno}, {events}")
                service = self.socket_to_service_map.get(fileno, None)

                if service is not None:
                    sock = self.get_socket_from_fileno(fileno)

                    if event & select.EPOLLIN:
                        c_connected, c_socket, c_wants_write = service.handle_readable(sock)
                        if not c_connected:
                            self.epoll_unregister(fileno)
                            continue
                        if c_socket is not None:
                            # add new client
                            self.register_socket(c_socket, service, False)
                        if c_wants_write:
                            self.epoll_unregister(fileno)
                            self.register_socket(fileno, service, True)
                            pass

                    if event & select.EPOLLOUT:
                        c_connected, c_wants_write = service.handle_writable(sock)
                        if not c_connected or not c_wants_write:
                            self.epoll_unregister(fileno)
                            if c_connected:
                                self.register_socket(fileno, service, False)
                            continue

                    if event & (select.EPOLLERR | select.EPOLLHUP):
                        crashed = service.handle_exceptions(sock)
                        if crashed:
                            self.services.remove(service)
                        else:
                            self.epoll_unregister(fileno)
                            continue


        log(f"HornPot terminates, no services (left).")
