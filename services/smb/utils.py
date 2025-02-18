import struct

#https://github.com/samba-team/samba/blob/7cae7aad1ca6dcd5e0a3a102f36af74fa49a2c2b/libcli/smb/smb_constants.h#L63

def VWV(vwv):
    if not isinstance(vwv, int) or vwv < 0:
        raise ValueError("Input must be a non-negative integer.")

    return vwv * 2


def memset(buffer, value, length):
    if not isinstance(buffer, bytearray):
        raise TypeError("buffer must be a bytearray")

    if length > len(buffer):
        raise ValueError("length exceeds buffer size")

    for i in range(length):
        buffer[i] = value


# https://github.com/samba-team/samba/blob/7cae7aad1ca6dcd5e0a3a102f36af74fa49a2c2b/lib/util/byteorder.h#L73

def SSVAL(buf, pos, val):
    """Put a 2 byte SMB value into a buffer."""
    struct.pack_into('<H', buf, pos, val)
    return 2

def SIVAL(buf, pos, val):
    """Put a 4 byte SMB value into a buffer."""
    struct.pack_into('<I', buf, pos, val)
    return 4

def SBVAL(buf, pos, val):
    """Put an 8 byte SMB value into a buffer."""
    struct.pack_into('<Q', buf, pos, val)
    return 8

def SSVALS(buf, pos, val):
    """Signed version of SSVAL() - put a signed 2 byte SMB value into a buffer."""
    struct.pack_into('<h', buf, pos, val)
    return 2

def SIVALS(buf, pos, val):
    """Signed version of SIVAL() - put a signed 4 byte SMB value into a buffer."""
    struct.pack_into('<i', buf, pos, val)
    return 4

def SBVALS(buf, pos, val):
    """Signed version of SBVAL() - put a signed 8 byte SMB value into a buffer."""
    struct.pack_into('<q', buf, pos, val)
    return 8





# https://github.com/samba-team/samba/blob/7cae7aad1ca6dcd5e0a3a102f36af74fa49a2c2b/lib/ldb/common/ldb_pack.c#L61



def _DATA_BYTE_CONST(data, pos):
    return data[pos]

def _DATA_BYTE(data, pos):
    return data[pos]

def PULL_LE_U8(data, pos):
    return _DATA_BYTE_CONST(data, pos)

def PULL_LE_I8(data, pos):
    return int.from_bytes([PULL_LE_U8(data, pos)], byteorder='little', signed=True)

def PULL_LE_U16(data, pos):
    return (PULL_LE_U8(data, pos) | (PULL_LE_U8(data, pos + 1) << 8))

def PULL_LE_I16(data, pos):
    return int.from_bytes(PULL_LE_U16(data, pos).to_bytes(2, byteorder='little'), byteorder='little', signed=True)

def PULL_LE_U32(data, pos):
    return (PULL_LE_U16(data, pos) | (PULL_LE_U16(data, pos + 2) << 16))

def PULL_LE_I32(data, pos):
    return int.from_bytes(PULL_LE_U32(data, pos).to_bytes(4, byteorder='little'), byteorder='little', signed=True)

def PULL_LE_U64(data, pos):
    return (PULL_LE_U32(data, pos) | (PULL_LE_U32(data, pos + 4) << 32))

def PULL_LE_I64(data, pos):
    return int.from_bytes(PULL_LE_U64(data, pos).to_bytes(8, byteorder='little'), byteorder='little', signed=True)


def _DATA_BYTE_CONST(data, pos):
    return data[pos]

def _DATA_BYTE(data, pos):
    return data[pos]

def CVAL(buf, pos):
    return int(_DATA_BYTE_CONST(buf, pos))

def CVAL_NC(buf, pos):
    return _DATA_BYTE(buf, pos)

def PVAL(buf, pos):
    return CVAL(buf, pos)

def SCVAL(buf, pos, val):
    buf[pos] = val & 0xFF



def _DATA_BYTE_CONST(data, pos):
    return data[pos]

def _DATA_BYTE(data, pos):
    return data[pos]

def PULL_BE_U8(data, pos):
    return _DATA_BYTE_CONST(data, pos)

def PULL_BE_I8(data, pos):
    return int.from_bytes([PULL_BE_U8(data, pos)], byteorder='big', signed=True)

def PULL_BE_U16(data, pos):
    return ((PULL_BE_U8(data, pos) << 8) | PULL_BE_U8(data, pos + 1))

def PULL_BE_I16(data, pos):
    return int.from_bytes(PULL_BE_U16(data, pos).to_bytes(2, byteorder='big'), byteorder='big', signed=True)

def PULL_BE_U32(data, pos):
    return ((PULL_BE_U16(data, pos) << 16) | PULL_BE_U16(data, pos + 2))

def PULL_BE_I32(data, pos):
    return int.from_bytes(PULL_BE_U32(data, pos).to_bytes(4, byteorder='big'), byteorder='big', signed=True)

def PULL_BE_U64(data, pos):
    return ((PULL_BE_U32(data, pos) << 32) | PULL_BE_U32(data, pos + 4))

def PULL_BE_I64(data, pos):
    return int.from_bytes(PULL_BE_U64(data, pos).to_bytes(8, byteorder='big'), byteorder='big', signed=True)

def _DATA_BYTE_CONST(data, pos):
    return data[pos]

def _DATA_BYTE(data, pos):
    return data[pos]

def PULL_LE_U8(data, pos):
    return _DATA_BYTE_CONST(data, pos)

def PULL_LE_I8(data, pos):
    return int.from_bytes([PULL_LE_U8(data, pos)], byteorder='little', signed=True)

def PULL_LE_U16(data, pos):
    return (PULL_LE_U8(data, pos) | (PULL_LE_U8(data, pos + 1) << 8))

def PULL_LE_I16(data, pos):
    return int.from_bytes(PULL_LE_U16(data, pos).to_bytes(2, byteorder='little'), byteorder='little', signed=True)

def PULL_LE_U32(data, pos):
    return (PULL_LE_U16(data, pos) | (PULL_LE_U16(data, pos + 2) << 16))

def PULL_LE_I32(data, pos):
    return int.from_bytes(PULL_LE_U32(data, pos).to_bytes(4, byteorder='little'), byteorder='little', signed=True)

# Push functions to write values back into the buffer
def PUSH_LE_U8(buf, pos, value):
    buf[pos] = value & 0xFF

def PUSH_LE_U16(buf, pos, value):
    PUSH_LE_U8(buf, pos, value & 0xFF)
    PUSH_LE_U8(buf, pos + 1, (value >> 8) & 0xFF)

def PUSH_LE_U32(buf, pos, value):
    PUSH_LE_U16(buf, pos, value & 0xFFFF)
    PUSH_LE_U16(buf,pos + 2,(value >> 16) & 0xFFFF)

# extract a 2 byte SMB value
def SVAL(buf,pos):
    return PULL_LE_U16(buf,pos)

#extract a 4 byte SMB value
def IVAL(buf,pos):
    return PULL_LE_U32(buf,pos)

def SSVALX(buf,pos,val):
    buf[pos] = val & 0xFF
    buf


# https://github.com/samba-team/samba/blob/7cae7aad1ca6dcd5e0a3a102f36af74fa49a2c2b/source4/libcli/raw/request.h#L43
class smb_request_buffer():

    def __init__(self, buffer: bytearray):
        # The raw SMB buffer, including the 4-byte length header
        self.buffer = buffer
        self.body = buffer

        # The size of the raw buffer, including 4-byte header
        self.size = len(buffer)

        # How much has been allocated - on reply the buffer is over-allocated to prevent too many realloc() calls
        self.allocated = 0

        # The start of the SMB header - this is always buffer + 4
        self.hdr = self.buffer[4:]

        # The command words and command word count. vwv points into the raw buffer
        self.vwv = None
        self.wct = 0

        # The data buffer and size. data points into the raw buffer
        self.data = buffer
        self.data_size = len(self.data)

        # Pointer used as a moving pointer into the data area of the packet.
        self.ptr = None

        # This would be used for range checking and aligning strings and buffers.
        self.bufinfo = {}



class RequestBufInfo:
    def __init__(self, data, mem_ctx: None):
        self.data = data
        self.data_size = len(data)
        self.mem_ctx = mem_ctx



#https://github.com/samba-team/samba/blob/a814f5d90a3fb85a94c9516dba224037e8fd76f1/source4/smb_server/smb/request.c#L639

def req_data_oob(bufinfo, src, length):
    # Placeholder for out-of-bounds check logic
    # This should check if 'src' and 'length' are valid within the context of 'bufinfo'
    return False  # Assume it's always in bounds for this example

def req_pull_blob(bufinfo, src, length):
    if length != 0 and req_data_oob(bufinfo, src, length):
        return False

# https://github.com/samba-team/samba/blob/7cae7aad1ca6dcd5e0a3a102f36af74fa49a2c2b/source4/smb_server/smb/request.c#L590
def req_pull_string(bufinfo, src, use_ucs2=False):
    if use_ucs2:
        return req_pull_ucs2(bufinfo, src)
    else:
        return req_pull_ascii(bufinfo, src)


def req_pull_ascii(bufinfo, src):
    try:
        end_index = src.index(0)  # Find null terminator
        # return always +1 to remove the \0
        return bytes(src[:end_index]).decode('ascii'), end_index+1
    except ValueError:
        return None, -1  # No null terminator found



def req_pull_ucs2(bufinfo, src):
    # Check if there's enough data for at least one UCS2 character (2 bytes)
    if len(src) < 2:
        return None, 0

    # Calculate the maximum length of the UCS2 string
    max_length = len(src)

    # Find the null terminator (U+0000)
    ucs2_end_index = None
    for i in range(0, max_length - 1, 2):  # Step by 2 bytes for UCS2
        if src[i] == 0 and src[i + 1] == 0:  # Null terminator found
            ucs2_end_index = i
            break

    if ucs2_end_index is None:
        ucs2_end_index = max_length - (max_length % 2)  # Use even length up to max

    # Extract the UCS2 string up to the null terminator
    ucs2_bytes = src[:ucs2_end_index]

    try:
        # Convert UCS2 bytes to UTF-8 string
        utf8_string = ucs2_bytes.decode('utf-16le')  # Assuming little-endian encoding
        return utf8_string, len(ucs2_bytes)
    except Exception as e:
        print(f"Error converting UCS2 to UTF-8: {e}")
        return None, 0




# https://github.com/samba-team/samba/blob/7cae7aad1ca6dcd5e0a3a102f36af74fa49a2c2b/source4/smb_server/smb/request.c#L610
def req_pull_ascii4(bufinfo, src):
    if len(src) == 0: # or src[0] != 0x04:  # Check if there's enough data and first byte is 0x04
        dest = ""
        return dest, 0

    # Consume the 0x4 byte
    src = src[1:]

    dest, ret = req_pull_string(bufinfo, src)

    if ret == -1:  # If no valid string was found
        dest = ""  # Set to empty string as per win2000 behavior
        return dest, 1

    return dest, ret + 1  # Return with null termination


