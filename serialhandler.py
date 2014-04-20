import struct

# use PPP frame format
FRAME_START_BYTE = 0x7E
FRAME_ESCAPE_BYTE = 0x7D
FRAME_ESCAPE_MASK = 0x20
FRAME_END_BYTE = 0x7E


PROTOCOL_CMD_LOG = 1,
PROTOCOL_CMD_STATUS = 2,
PROTOCOL_CMD_THROTTLE = 3


class Frame(object):
    def __init__(self, port):
        self.port = port

    def __enter__(self):
        self.port.write([FRAME_START_BYTE])
        return self
    
    def write(self, bytes):
        print(bytes)
        escaped = bytearray()
        for b in bytes:
            if b in (FRAME_START_BYTE, FRAME_ESCAPE_BYTE):
                escaped.append(FRAME_ESCAPE_BYTE)
                escaped.append(b ^ FRAME_ESCAPE_MASK)
            else:
                escaped.append(b)
        self.port.write(escaped)

    def __exit__(self, type, value, traceback):
        self.port.write([FRAME_END_BYTE])


class SerialProtocol(object):
    def __init__(self, port):
        self.frame = Frame(port)

    def cmd(self, cmd_id, arg):
        with self.frame as frame:
            frame.write(struct.pack('>BH', cmd_id, arg))

    def throttle(self, power):
        self.cmd(PROTOCOL_CMD_THROTTLE, power)

