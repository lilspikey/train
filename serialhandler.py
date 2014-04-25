import struct
import threading

# use PPP frame format
FRAME_START_BYTE = 0x7E
FRAME_ESCAPE_BYTE = 0x7D
FRAME_ESCAPE_MASK = 0x20
FRAME_END_BYTE = 0x7E


PROTOCOL_CMD_LOG = 1
PROTOCOL_CMD_STATUS = 2
PROTOCOL_CMD_THROTTLE_FWD = 3
PROTOCOL_CMD_THROTTLE_REV = 4
PROTOCOL_CMD_TURNOUT_LEFT = 5
PROTOCOL_CMD_TURNOUT_RIGHT = 6
PROTOCOL_CMD_DECOUPLER_UP = 7
PROTOCOL_CMD_DECOUPLER_DOWN = 8



class SerialClosedException(Exception):
    pass


class Frame(object):
    def __init__(self, port):
        self.port = port

    def __enter__(self):
        self.port.write([FRAME_START_BYTE])
        return self
    
    def write(self, bytes):
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
    
    def _read(self, stop):
        while True:
            b = self.port.read()
            if b:
                return b[0]
            elif stop.is_set():
                raise SerialClosedException("Serial port closed")

    def read_frame(self, stop):
        while True:
            b = self._read(stop)
            if b == FRAME_START_BYTE:
                break

        frame = bytearray()
        while True:
            b = self._read(stop)
            if b == FRAME_ESCAPE_BYTE:
                e = self._read() ^ FRAME_ESCAPE_MASK
                frame.append(e)
            elif b == FRAME_END_BYTE:
                break
            else:
                frame.append(b)
        return frame


class SerialProtocol(object):
    def __init__(self, port):
        self.frame = Frame(port)
        self.stop = threading.Event()
        reader = threading.Thread(target=self.read_frames)
        reader.start()
    
    def __del__(self):
        self.stop.set()

    def read_frames(self):
        print("Reading frames")
        while not self.stop.is_set():
            try:
                frame = self.frame.read_frame(self.stop)
                print(frame)
            except SerialClosedException:
                pass

    def cmd(self, cmd_id, arg):
        with self.frame as frame:
            frame.write(struct.pack('>BH', cmd_id, arg))

    def throttle_forward(self, power):
        power = max(0, min(1024, power));
        self.cmd(PROTOCOL_CMD_THROTTLE_FWD, power)

    def throttle_reverse(self, power):
        power = max(0, min(1024, power));
        self.cmd(PROTOCOL_CMD_THROTTLE_REV, power)

    def turnout_left(self):
        self.cmd(PROTOCOL_CMD_TURNOUT_LEFT, 0)

    def turnout_right(self):
        self.cmd(PROTOCOL_CMD_TURNOUT_RIGHT, 0)

    def decoupler_up(self):
        self.cmd(PROTOCOL_CMD_DECOUPLER_UP, 0)

    def decoupler_down(self):
        self.cmd(PROTOCOL_CMD_DECOUPLER_DOWN, 0)

