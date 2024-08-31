import codecs
import re
import socket

from message_handler import bytes_to_string
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
    b"\r\n"
    b"\r\n"

)


# Example ELF header for an x86_64 binary
elf_header = bytes([
    0x7f, 0x45, 0x4c, 0x46,  # ELF Magic Number
    0x02, 0x01, 0x01, 0x00,  # 64-bit, little-endian, ELF version 1
    0x00, 0x00, 0x00, 0x00,  # ABI and padding
    0x00, 0x00, 0x00, 0x00,  # Padding
    0x02, 0x00, 0x3e, 0x00,  # Type (Executable), Machine (x86_64)
    0x01, 0x00, 0x00, 0x00,  # ELF version
    0x78, 0x00, 0x40, 0x00,  # Entry point address
    0x00, 0x00, 0x00, 0x00,  # Program header table offset
    0x40, 0x00, 0x00, 0x00,  # Section header table offset
    0x00, 0x00, 0x00, 0x00,  # Flags
    0x40, 0x00, 0x38, 0x00,  # ELF header size, Program header entry size
    0x01, 0x00, 0x00, 0x00,  # Program header entry count, Section header entry size
    0x00, 0x00, 0x00, 0x00   # Section header entry count, Section header string table index
])

# Dummy ELF program data
program_data = bytes([0x48, 0x31, 0xC0, 0xC3])  # Assembly for 'xor rax, rax; ret'

# Combine ELF header with program data to create the full executable binary response
fake_exe_response = elf_header + program_data



class SessionTelnet(SessionBase):


    def __init__(self, s: socket, service):

        super().__init__(s, service)
        self.message_queue = welcome_message
        self.message_queue += IAC + WILL + ECHO  # Indicate that server will handle echo
        self.message_queue += IAC + WILL + SUPPRESS_GO_AHEAD  # Suppress go-ahead
        self.message_queue += b'$ '


    def simulate_bash(self, msg):

        end = True

        msg = msg.strip()

        if msg == "whoami":
            self.message_queue += b"root"

        elif msg == "pwd":
            self.message_queue += b"/home/root"

        elif msg == "uname -a":
            self.message_queue += b"Linux ubuntu 6.8.0-31-generic #31-Ubuntu SMP PREEMPT_DYNAMIC Sat Apr 20 00:40:06 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux"

        elif "echo" in msg:
            # attacks using echo -e "SOMEHEX" to check if the bash is working,
            # so we need to make sure we send them this string in ASCII back

            index = msg.find("echo ")
            if index != -1:
                msg =  msg[index:]

            msg = msg.replace("echo", "").strip()
            if msg.lower().startswith("-e"):
                msg = msg.replace("-e", "").strip()
                try:
                    #remove "

                    msg = msg.replace("\\\\", "\\").replace("\"", "")
                    decoded_string = codecs.decode(msg, 'unicode_escape')
                    self.message_queue += decoded_string.encode('ascii')
                except (UnicodeDecodeError, ValueError) as e:
                    print(f"Decoding failed: {e}")


        elif msg == "ls":
            self.message_queue += b".ssh  .bashrc  .bash_history"

        elif msg.startswith("cd "):
            pass

        elif msg == ("ping"):
            self.message_queue += b"ping: usage error: Destination address required"

        elif msg.startswith("sh"):
            pass

        elif msg == "root":
            self.message_queue += b"password: "
            end = False

        elif msg == "while read i;do busybox":
            # "simulates busybox"
            pass

        elif msg == "date":
            import datetime
            current_date = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
            self.message_queue += current_date.encode()

        elif msg.startswith("cat "):
            if msg == "cat /proc/self/exe":
                self.message_queue += fake_exe_response
            else:
                self.message_queue += b"Oh no, dont read my secrets pls"

        elif msg == "uptime":
            self.message_queue += b" 10:23:01 up 2 days,  3:45,  1 user,  load average: 0.05, 0.02, 0.01"

        else:
            pass
            #self.message_queue += b"command not found"

        return end

    def read_from_socket(self):
        msg = self._read_from_socket()
        if msg is None:
            return False

        msg = bytes_to_string(msg)
        if msg is None:
            return True

        commands = re.split(r';|\|\|', msg)
        commands = [cmd.strip() for cmd in commands]

        append_end = True
        for command in commands:
            if len(command) == 0:
                continue
            append_end &= self.simulate_bash(command)
            if append_end:
                self.message_queue += b"\r\n"

        if append_end:
            self.message_queue += b"$ "

        return True