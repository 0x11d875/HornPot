import socket
from services.Session import SessionBase
from services.smb.SMB1 import SMB1_parser


class SessionSMB(SessionBase):

    def __init__(self, s: socket, service):
        super().__init__(s, service)
        self.smb1_parser = SMB1_parser()


    def read_from_socket(self):
        msg = self._read_from_socket()
        if msg is None:
            return False

        resp = b''
        try:
            resp = self.smb1_parser.create_smb_response(msg)
            if resp is not None:
                self.message_queue += bytes(resp)
        except:
            return False


        return True