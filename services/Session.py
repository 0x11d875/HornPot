from queue import Queue

from SimpleSimpleSocket import SimpleSocket
from logger import log, Database, get_timestamp


class SessionBase:

    def __init__(self, ss: SimpleSocket):
        self.ss: SimpleSocket = ss

        # log data
        self.session_start = get_timestamp()
        self.last_active = get_timestamp()
        self.conservation = []


        log(f"New session from {self.ss.ip}:{self.ss.port} at port {self.ss.port}.", self.__class__.__name__)

        self.write_queue = []
        self.connected = True

    def wants_write(self) -> bool:
        return len(self.write_queue) != 0

    def read_from_socket(self):
        msg = self.ss.recv()
        if msg is None: # error
            return False

        if len(msg) <= 0: # terminating
            return False

        self.last_active = get_timestamp()
        self.conservation.append(f'[r][{get_timestamp()}]: {msg}')
        log(f"Read from {self.ss.ip}:{self.ss.port} '{msg}'.", self.__class__.__name__)
        # TODO log message and handel it
        return True

    def send_message(self) -> bool:
        send = self.ss.send(self.write_queue)
        if send <= 0: # terminate
            return False

        self.last_active = get_timestamp()
        self.conservation.append(f'[t][{get_timestamp()}]: {self.write_queue[:send]}')
        self.write_queue = self.write_queue[send:]
        return True
