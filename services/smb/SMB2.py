
from services.smb.smb1_constants import *
from services.smb.smb2_constants import *
from services.smb.utils import *

# https://github.com/samba-team/samba/blob/7cae7aad1ca6dcd5e0a3a102f36af74fa49a2c2b/source4/smb_server/smb2/negprot.c#L278
# reply to a SMB negprot request with dialect "SMB 2.002"
def smb2srv_reply_smb_negprot(req):
    body_fixed_size = 0x26
    size = NBT_HDR_SIZE+SMB2_HDR_BODY+body_fixed_size
    res = smb_request_buffer(bytearray(size))
    res.hdr = res.buffer[NBT_HDR_SIZE:]
    res.body = res.hdr[SMB2_HDR_BODY:]

    #smb2srv_setup_bufinfo(req)

    SIVAL(res.hdr, 0, SMB2_MAGIC)
    SSVAL(res.hdr, SMB2_HDR_LENGTH, SMB2_HDR_BODY)
    SSVAL(res.hdr, SMB2_HDR_EPOCH, 0)
    SIVAL(res.hdr, SMB2_HDR_STATUS, 0)
    SSVAL(res.hdr, SMB2_HDR_OPCODE, SMB2_OP_NEGPROT)
    SSVAL(res.hdr, SMB2_HDR_CREDIT, 0)
    SIVAL(res.hdr, SMB2_HDR_FLAGS, 0)
    SIVAL(res.hdr, SMB2_HDR_NEXT_COMMAND, 0)
    SBVAL(res.hdr, SMB2_HDR_MESSAGE_ID, 0)
    SIVAL(res.hdr, SMB2_HDR_PID, 0)
    SIVAL(res.hdr, SMB2_HDR_TID, 0)
    SBVAL(res.hdr, SMB2_HDR_SESSION_ID, 0)
    #memset(res.hdr[SMB2_HDR_SIGNATURE:], 0, 16)

    # this seems to be a bug, they use 0x24 but the length is 0x26
    SSVAL(res.hdr, SMB2_HDR_BODY+0x00, 0x24)
    
    SSVAL(res.hdr, SMB2_HDR_BODY+0x02, 1)
    #memset(res.body[0x04:], 0, 32)
    SSVAL(res.hdr, SMB2_HDR_BODY+0x24, SMB2_DIALECT_REVISION_202)


    print(f"Ready response: {res.hdr}")





# https://github.com/samba-team/samba/blob/7cae7aad1ca6dcd5e0a3a102f36af74fa49a2c2b/source4/smb_server/smb/negprot.c#L464
def reply_smb2(rq_in: smb_request_buffer, choice: int):
    pass


# https://github.com/samba-team/samba/blob/7cae7aad1ca6dcd5e0a3a102f36af74fa49a2c2b/source4/smb_server/smb/negprot.c#L513
# while the request contains supported protocols, the function adds every supported function to the response.
# the original implementation does some checks like 'is this the first negprot request' and so on
# but we dont care and just say we support everything
def smbsrv_reply_negprot(rq_in: smb_request_buffer):
    pass


