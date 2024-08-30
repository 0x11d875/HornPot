import socket

from services.Session import SessionBase

# Telnet control characters
IAC = b'\xff'
DO = b'\xfd'
WILL = b'\xfb'
ECHO = b'\x01'
SUPPRESS_GO_AHEAD = b'\x03'

welcome_message = (
    b"Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.8.0-31-generic x86_64)\r\n"
    b"\r\n"
    b" * Documentation:  https://help.ubuntu.com\r\n"
    b" * Management:     https://landscape.canonical.com\r\n"
    b" * Support:        https://ubuntu.com/pro\r\n"
    b"\r\n"
    b"\r\n"
    b"Expanded Security Maintenance for Applications is not enabled.\r\n"
    b"\r\n"
    b"0 updates can be applied immediately.\r\n"
    b"\r\n"
    b"Enable ESM Apps to receive additional future security updates.\r\n"
    b"See https://ubuntu.com/esm or run: sudo pro status\r\n"
    b"\r\n"
    b"\r\n"
    b"The list of available updates is more than a week old.\r\n"
    b"To check for new updates run: sudo apt update\r\n"
    b"Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings\r\n"
    b"\r\n"
    b"\r\n"

)


class SessionTelnet(SessionBase):


    def __init__(self, s: socket, service):

        super().__init__(s, service)
        self.message_queue = welcome_message
        self.message_queue += IAC + WILL + ECHO  # Indicate that server will handle echo
        self.message_queue += IAC + WILL + SUPPRESS_GO_AHEAD  # Suppress go-ahead
        self.message_queue += b'$ '


    def read_from_socket(self):
        msg = self._read_from_socket()
        if msg is None:
            return False

        if msg.lower() == b"whoami\n":
            self.message_queue += b"root\r\n$ "
        elif msg.lower() == b"pwd\n":
            self.message_queue += b"/home/root\r\n$ "
        elif msg.lower() == b"ls\n":
            self.message_queue += b".ssh  .bashrc  .bash_history\r\n$ "
        elif msg.lower().startswith(b"cd "):
            self.message_queue += b"$ "
        elif msg.lower() == b"date\n":
            import datetime
            current_date = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
            self.message_queue += current_date.encode() + b"\r\n$ "
        elif msg.lower().startswith(b"cat "):
            self.message_queue += b"Oh no, dont read my secrets pls\r\n$ "
        elif msg.lower() == b"uptime\n":
            self.message_queue += b" 10:23:01 up 2 days,  3:45,  1 user,  load average: 0.05, 0.02, 0.01\r\n$ "

        else:
            self.message_queue += b"command not found\r\n$ "

        return True