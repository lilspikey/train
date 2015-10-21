import struct
import threading
import collections
import time

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
PROTOCOL_CMD_LIGHT1_ON = 9
PROTOCOL_CMD_LIGHT1_OFF = 10
PROTOCOL_CMD_LIGHT2_ON = 11
PROTOCOL_CMD_LIGHT2_OFF = 12


class SerialClosedException(Exception):
    pass


class Frame(object):
    def __init__(self, port):
        self.port = port
        self._incoming_bytes = collections.deque()

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
            if self._incoming_bytes:
                return self._incoming_bytes.popleft()
            num = max(1, self.port.inWaiting())
            b = self.port.read(size=num)
            if b:
                self._incoming_bytes.extend(b)
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
                e = self._read(stop) ^ FRAME_ESCAPE_MASK
                frame.append(e)
            elif b == FRAME_END_BYTE:
                break
            else:
                frame.append(b)
        return frame


class SerialProtocol(object):
    def __init__(self, port, callback):
        self.frame = Frame(port)
        self.stop = threading.Event()
        self.callback = callback
        reader = threading.Thread(target=self.read_frames)
        reader.start()
    
    def __del__(self):
        self.stop.set()
    
    def _read_string(self, bytes):
        len, data = bytes[0], bytes[1:]
        return data[:len].decode('ascii'), data[len:]

    def _read_int(self, bytes):
        unpacked = struct.unpack('>H', bytes)
        i = unpacked[0]
        return i, None

    def decode_frame(self, frame):
        cmd, data = frame[0], frame[1:]
        if cmd == PROTOCOL_CMD_LOG:
            log, _ = self._read_string(data)
            print('LOG:', log)
        elif cmd == PROTOCOL_CMD_STATUS:
            key, remaining = self._read_string(data)
            value, _ = self._read_int(remaining)
            if key == 'turnout':
                value = 'left' if value else 'right';
            elif key == 'decoupler':
                value = 'up' if value else 'down';
            elif key.startswith('sensor') or key.startswith('light'):
                value = True if value else False
            self.callback(key, value)

    def read_frames(self):
        time.sleep(1.5)
        while not self.stop.is_set():
            try:
                frame = self.frame.read_frame(self.stop)
                self.decode_frame(frame)
            except SerialClosedException:
                pass

    def cmd(self, cmd_id, arg):
        with self.frame as frame:
            frame.write(struct.pack('>BH', cmd_id, arg))

    def throttle_forward(self, power):
        power = max(0, min(1024, int(power)));
        self.cmd(PROTOCOL_CMD_THROTTLE_FWD, power)

    def throttle_reverse(self, power):
        power = max(0, min(1024, int(power)));
        self.cmd(PROTOCOL_CMD_THROTTLE_REV, power)

    def turnout_left(self):
        self.cmd(PROTOCOL_CMD_TURNOUT_LEFT, 0)

    def turnout_right(self):
        self.cmd(PROTOCOL_CMD_TURNOUT_RIGHT, 0)

    def decoupler_up(self):
        self.cmd(PROTOCOL_CMD_DECOUPLER_UP, 0)

    def decoupler_down(self):
        self.cmd(PROTOCOL_CMD_DECOUPLER_DOWN, 0)

    def light1_on(self):
        self.cmd(PROTOCOL_CMD_LIGHT1_ON, 0)

    def light1_off(self):
        self.cmd(PROTOCOL_CMD_LIGHT1_OFF, 0)
    
    def light2_on(self):
        self.cmd(PROTOCOL_CMD_LIGHT2_ON, 0)

    def light2_off(self):
        self.cmd(PROTOCOL_CMD_LIGHT2_OFF, 0)


class DummyPort(object):
    '''
       This is used to provide a surrogate for the real serial port
       and arduino, when they aren't connected
    '''
    def __init__(self):
        class InternalPort(object):
            def __init__(self):
                self._bytes_in = []
                self._bytes_out = []

            def inWaiting(self):
                if self._bytes_in:
                    return len(self._bytes_in[0])
                return 0

            def read(self, size=None):
                if self._bytes_in:
                    return self._bytes_in.pop(0)
                from time import sleep
                sleep(0.1)
                return None

            def write(self, bytes):
                self._bytes_out.append(bytes)

        self._int_port = InternalPort()
        self.stop = threading.Event()
        self.frame = Frame(self._int_port)
        self._frame_lock = threading.RLock()
        reader = threading.Thread(target=self.read_frames)
        reader.daemon = True
        reader.start()
        input = threading.Thread(target=self.read_input)
        input.daemon = True
        input.start()
    
    def read_input(self):
        print("Commands:")
        print(" decouple-test")
        while True:
            text = input()
            text = text.strip()
            if text == 'decouple-test':
                self.write_status_int('sensor1', 1)
                self.write_status_int('sensor2', 1)
                from time import sleep
                sleep(3)
                self.write_status_int('sensor1', 0)
                self.write_status_int('sensor3', 1)
                sleep(3)
                self.write_status_int('sensor2', 0)
                self.write_status_int('sensor3', 0)
                self.write_status_int('decoupler', 0)
    
    def write_status_int(self, sensor, value):
        self.write_status(sensor, struct.pack('>H', value))

    def read(self, size=None):
        if self._int_port._bytes_out:
            return self._int_port._bytes_out.pop(0)
        else:
            from time import sleep
            sleep(0.1)    
            return None
    
    def inWaiting(self):
        if self._int_port._bytes_out:
            return len(self._int_port._bytes_out[0])
        return 0
    
    def write_status(self, key, value):
        with self._frame_lock:
            with self.frame as frame:
                key = key.encode('ascii')
                frame.write(struct.pack('>BB', PROTOCOL_CMD_STATUS, len(key)))
                frame.write(key)
                frame.write(value)

    def decode_frame(self, frame):
        cmd, data = frame[0], frame[1:]
        if cmd == PROTOCOL_CMD_THROTTLE_FWD:
            self.write_status_int('forward', 1)
            self.write_status('power', data)
        elif cmd == PROTOCOL_CMD_THROTTLE_REV:
            self.write_status_int('forward', 0)
            self.write_status('power', data)
        elif cmd == PROTOCOL_CMD_TURNOUT_LEFT:
            self.write_status_int('turnout', 1)
        elif cmd == PROTOCOL_CMD_TURNOUT_RIGHT:
            self.write_status_int('turnout', 0)
        elif cmd == PROTOCOL_CMD_DECOUPLER_UP:
            self.write_status_int('decoupler', 1)
        elif cmd == PROTOCOL_CMD_DECOUPLER_DOWN:
            self.write_status_int('decoupler', 0)

    def read_frames(self):
         while not self.stop.is_set():
            try:
                frame = self.frame.read_frame(self.stop)
                self.decode_frame(frame)
            except SerialClosedException:
                pass

    def write(self, bytes):
        self._int_port._bytes_in.append(bytes)

