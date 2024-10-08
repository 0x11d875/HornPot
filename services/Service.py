import socket
from datetime import datetime

from influx import Influx
from logger import log, Database, get_timestamp, TIMEFORMAT
from services.Session import SessionBase


class Service:

    def __init__(self, name: str, ip: str, port: int, db: Database, config, session=SessionBase,):
        self.name: str = name
        self.ip: str = ip
        self.port: int = port

        self.db: Database = db
        self.config: dict = config

        log(f'Service {self.name} running on port {self.port}')

        self.server = socket.create_server(address=(self.ip, self.port), family=socket.AF_INET6, backlog=5,
                                           reuse_port=True, dualstack_ipv6=True)

        # FIXME: could be blocking
        self.server.setblocking(False)

        # lookup dict to match socket -> Session
        self.s_to_session: dict[socket: SessionBase] = {}
        self.session = session

    def check_quota(self):
        if self.config.config.get('quota', False):
            quota = self.config.config.get('quota')

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

                if quota.get('tx', False) and session.num_sent_bytes > quota['tx']:
                    killed_sessions.append((session, 'killed quota tx'))
                    continue

                if quota.get('rx', False) and session.num_received_bytes > quota['rx']:
                    killed_sessions.append((session, 'killed quota rx'))
                    continue

            for kill_session in killed_sessions:
                self._terminate_session(kill_session[0].s, kill_session[1])
            return killed_sessions


    def socket_to_session(self, s: socket) -> SessionBase | None:
        if s == self.server:
            return self.server
        return self.s_to_session.get(s, None)

    def __accept_client(self) -> socket:
        try:
            # FIXME: client_address is unused
            client_socket, client_address = self.server.accept()
        except OSError as e:
            # TODO: logging
            return None
        # TODO: Make client_socket non-blocking
        if client_socket is not None:
            session = self.session(client_socket, self)

            if self.config.influx_enabled:
                influx_client = Influx(self.config)
                influx_client.add_session(session)

            if session.connected:
                self.s_to_session[client_socket] = session
            return client_socket

    def __close_client(self, s: socket) -> None:
        self.s_to_session.pop(s)

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
        if session is None:
            return

        self.s_to_session.pop(s)

        if session.termination_reason == "":
            session.termination_reason = reason

        self.db.add_session(session)
        session.disconnect()


    def handle_readable(self, s: socket):
        client_connected = False
        client_socket = None
        client_wants_write = False
        if s is self.server:  # handle a new connection
            client_connected = True
            client_socket = self.__accept_client()
            session = self.socket_to_session(client_socket)

        else:
            session = self.socket_to_session(s)
            if session is not None:
                client_connected = session.read_from_socket()
                if not client_connected:
                    self._terminate_session(s)
                    return False, None, False
                try:
                    self.db.handle_message(session, session.last_received_message)
                except Exception as e:
                    log(f"Unable to download link: {e}")

        if session is not None and session.wants_write():
            client_wants_write = True
                
        return client_connected, client_socket, client_wants_write
    


    def handle_writable(self, s: socket) -> bool:
        client_connected = False
        client_wants_to_write = False

        session = self.socket_to_session(s)

        if session is not None:
            success = session.send_message()
            if not success:
                self._terminate_session(s)
                return client_connected, client_wants_to_write
            client_connected = True

        client_wants_to_write = session.wants_write()
        return client_connected, client_wants_to_write

    # Returns True, iff service crashed due to server socket error
    def handle_exceptions(self, s: socket) -> bool:
        if s is self.server:
            return True

        self._terminate_session(s)
        return False
