from datetime import datetime
from socket import socket

from SimpleSimpleSocket import SimpleSocket
from logger import log, Database, get_timestamp, TIMEFORMAT
from services.Session import SessionBase


class ServiceBase:

    def __init__(self, name: str, ip: str, port: int, db:Database, config, session=SessionBase):
        self.name: str = name
        self.ip: str = ip
        self.port: int = port

        self.db: Database = db
        self.config: dict= config

        log(f'Service {self.name} running on port {self.port}')

        self.serverSo = SimpleSocket((ip, port), True)
        self.serverSo.bind_listen_and_go(ip, port)

        # lookup dict to match socket -> Session
        self.s_to_session: dict[socket: SessionBase] = {}
        self.session = session

    def check_quota(self):
        if self.config.get('quota', False):
            quota = self.config.get('quota')

            now = datetime.strptime(get_timestamp(), TIMEFORMAT)
            killed_sessions = []
            for session in self.s_to_session.values():
                active_since = datetime.strptime(session.session_start, TIMEFORMAT)
                if quota.get('active', False) and abs((now - active_since).total_seconds()) > quota['active']:
                    killed_sessions.append((session, 'killed quota active'))
                    continue

                last_active = datetime.strptime(session.session_start, TIMEFORMAT)
                if quota.get('idle', False) and abs((now - last_active).total_seconds()) > quota['idle']:
                    killed_sessions.append((session, 'killed quota idle'))
                    continue

                if quota.get('tx', False) and session.ss.tx > quota['tx']:
                    killed_sessions.append((session, 'killed quota tx'))
                    continue

                if quota.get('rx', False) and session.ss.tx > quota['rx']:
                    killed_sessions.append((session, 'killed quota rx'))
                    continue

            for kill_session in killed_sessions:
                self._terminate_session(kill_session[0].ss.socket, kill_session[1])


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
            self.s_to_session[ss.socket] = self.session(ss, self.serverSo.port)

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

    def _terminate_session(self, s: socket, reason=None) -> None:
        session = self.socket_to_session(s)
        if session is not None:
            self.s_to_session.pop(s)

        conservation = session.conservation
        if reason:
            conservation.append(f"[c][{get_timestamp()}]: Connection terminated duo to {reason}")

        self.db.add_session(session.session_start, session.ss.ip, session.ss.port, conservation)


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
