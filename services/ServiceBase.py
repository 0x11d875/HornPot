from socket import socket

from SimpleSimpleSocket import SimpleSocket
from logger import log, Database
from services.Session import SessionBase


class ServiceBase:

    def __init__(self, name: str, ip: str, port: int, db:Database, session=SessionBase):
        self.name: str = name
        self.ip: str = ip
        self.port: int = port

        self.db: Database = db

        log(f'Service {self.name} running on port {self.port}')

        self.serverSo = SimpleSocket((ip, port), True)
        self.serverSo.bind_listen_and_go(ip, port)

        # lookup dict to match socket -> Session
        self.s_to_session: dict[socket: SessionBase] = {}
        self.session = session

    def socket_to_session(self, s: socket) -> SessionBase | SimpleSocket | None:
        if s == self.serverSo.socket:
            return self.serverSo
        return self.s_to_session.get(s, None)

    def __simple_socket_to_socket(self, ss: SimpleSocket) -> socket | None:
        for key, value in self.s_to_session.items():
            if value == ss:
                return key
        return None

    def __accept_client(self) -> None:
        ss = self.serverSo.accept()
        if ss is not None:
            self.s_to_session[ss.socket] = self.session(ss)

    def __close_client(self, ss: SimpleSocket) -> None:
        self.s_to_session.pop(self.__simple_socket_to_socket(ss))

    def get_all_handled_sockets(self) -> list[socket]:
        return list(self.s_to_session.keys())

    def get_all_needs_write_sockets(self) -> list[socket]:
        needs_write = []
        for s, session in self.s_to_session.items():
            if session.wants_write():
                needs_write.append(s)
        return needs_write

    def _terminate_session(self, s: socket) -> None:
        session = self.socket_to_session(s)
        if session is not None:
            self.s_to_session.pop(s)

        self.db.add_session(session.session_start, session.ss.ip, session.ss.port, session.conservation)
        print(session.conservation)


    def handle_readable(self, s: socket):
        if s is self.serverSo.socket:  # handle a new connection
            self.__accept_client()
            return

        session = self.socket_to_session(s)
        if session is not None:
            success = session.read_from_socket()
            if not success:
                self._terminate_session(s)


    def handle_writable(self, s: socket):
        session = self.socket_to_session(s)
        if session is not None:
            success = session.send_message()
            if not success:
                self._terminate_session(s)

    # Returns True, if service crashed duo to server socket error
    def handle_exeptional(self, s: socket) -> bool:
        if s is self.serverSo.socket:
            return True

        self._terminate_session(s)
        return False
