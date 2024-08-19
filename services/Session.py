import socket
from logger import log, get_timestamp


class SessionBase:

    def __init__(self, s: socket):
        self.s: socket = s

        self.own_ip6, self.own_port6, self.own_ip4, self.own_port4 = self.s.getsockname()
        self.remote_ip6, self.remote_port6, self.remote_ip4, self.remote_port4 = self.s.getpeername()

        # log data
        self.session_start = get_timestamp()
        self.last_active = get_timestamp()
        self.conversation = []

        self.message_queue: str = ""
        self.connected = True

        self.num_sent_bytes = 0
        self.num_received_bytes = 0

        log(f"New session from {self.remote_ip6}:{self.remote_port6} at port {self.own_port6}.", self.__class__.__name__)

    def __del__(self):
        log(f"Disconnecting client {self.remote_ip6}:{self.remote_port6} at port {self.own_port6}.",
            self.__class__.__name__)
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def wants_write(self) -> bool:
        return len(self.message_queue) != 0

    def read_from_socket(self):
        try:
            msg = self.s.recv(4096)
        except OSError as e:
            # TODO: logging
            return False

        # error -> could not have been readable after select
        if msg is None:
            return False

        # client disconnect
        if len(msg) == 0:
            return False

        self.num_received_bytes += len(msg)

        self.last_active = get_timestamp()
        self.conversation.append(f'[r][{get_timestamp()}]: {msg}')
        log(f"Read from {self.remote_ip6}:{self.remote_port6} '{msg}'.", self.__class__.__name__)
        # TODO log message and handle it
        return True

    def send_message(self) -> bool:
        try:
            sent = self.s.send(self.message_queue)
        except OSError as e:
            # TODO: logging
            return False

        # error -> could not have been writable after select
        if sent <= 0:
            return False

        self.num_sent_bytes += sent

        self.last_active = get_timestamp()
        self.conversation.append(f'[t][{get_timestamp()}]: {self.message_queue[:sent]}')
        self.message_queue = self.message_queue[sent:]
        return True
