# use PPP frame format
FRAME_START_BYTE = 0x7E
FRAME_ESCAPE_BYTE = 0x7D
FRAME_ESCAPE_MASK = 0x20
FRAME_END_BYTE = 0x7E


class Frame(object):
    def __init__(self, port):
        self.port = port

    def __enter__(self):
        self.port.write(FRAME_START_BYTE)
        return self
    
    def write(self, *bytes):
        escaped = bytearray()
        for b in bytes:
            if b in (FRAME_START_BYTE, FRAME_ESCAPE_BYTE):
                escape.append(FRAME_ESCAPE_BYTE)
                escape.append(b ^ FRAME_ESCAPE_MASK)
            else:
                escape.append(b)
        self.port.write(escaped)

    def __exit__(self, type, value, traceback):
        self.port.write(FRAME_END_BYTE)


class SerialProtocol(object):
    def __init__(self, port):
        self.frame = Frame(port)

    def cmd(self, cmd_id, arg):
        with self.frame as frame:
            frame.write(cmd_id, arg)


