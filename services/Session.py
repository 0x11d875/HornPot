import socket


from logger import log, get_timestamp



class SessionBase:

    def __init__(self, s: socket, service):

        self.service = service
        self.s: socket = s
        self.connected = True

        self.session_start = get_timestamp()
        self.last_active = get_timestamp()
        self.session_end = None
        self.conversation = []
        self.last_received_message = None
        self.downloads = []

        self.message_queue: bytes = b''

        self.num_sent_bytes = 0
        self.num_received_bytes = 0
        self.num_received = 0
        self.num_send = 0
        self.termination_reason = ""

        try:
            self.own_ip6, self.own_port6, self.own_ip4, self.own_port4 = self.s.getsockname()
            self.remote_ip6, self.remote_port6, self.remote_ip4, self.remote_port4 = self.s.getpeername()
            log(f"Connected: {self.remote_ip6}:{self.remote_port6}.",
                f"{self.__class__.__name__}:{self.service.port}")
        except OSError:
            # socket may be not connected
            self.session_end = get_timestamp()
            self.termination_reason = "Abort Connection"
            self.connected = False


    def disconnect(self):
        try:
            log(f"Disconnected: {self.remote_ip6}:{self.remote_port6}.", f'{self.__class__.__name__}:{self.service.port}')
        except Exception as e:
            print(f"ERROR {e}")
            pass
        return
        # ignore shutdown, otherwise fd -1 problems using epoll.unregister
        try:
            self.s.shutdown(socket.SHUT_RDWR)
        except:
            pass
        try:
            self.s.close()
        except:
            pass


    def wants_write(self) -> bool:
        return len(self.message_queue) != 0

    def _read_from_socket(self) -> bytes | None:
        try:
            msg = self.s.recv(4096)
        except OSError as e:
            self.termination_reason = f"Read error {e}."
            return None

        # error -> could not have been readable after select
        if msg is None:
            self.termination_reason = f"Read None."
            return None

        # client disconnect
        if len(msg) == 0:
            self.termination_reason = f"Read length 0."
            return None

        self.num_received_bytes += len(msg)

        self.last_active = get_timestamp()
        self.conversation.append(f'[r][{get_timestamp()}]: {msg}')
        log(f"[r]{self.remote_ip6}:{self.remote_port6} '{msg}'.", f'{self.__class__.__name__}:{self.service.port}')
        self.last_received_message = msg
        return msg

    def read_from_socket(self) -> bool:
        msg = self._read_from_socket()
        if msg is None:
            return False
        return True


    def send_message(self) -> bool:
        try:
            sent = self.s.send(self.message_queue)
        except OSError as e:
            self.termination_reason = f"Send exception {e}."
            return False

        # error -> could not have been writable after select
        if sent <= 0:
            self.termination_reason = f"Send length {sent}."
            return False

        log(f"[t]{self.remote_ip6}:{self.remote_port6} '{self.message_queue[:sent]}'.", f'{self.__class__.__name__}:{self.service.port}')

        self.num_sent_bytes += sent

        self.last_active = get_timestamp()
        self.conversation.append(f'[t][{get_timestamp()}]: {self.message_queue[:sent]}')
        self.message_queue = self.message_queue[sent:]
        return True
