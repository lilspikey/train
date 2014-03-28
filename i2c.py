import os
from fcntl import ioctl

# bare minimal i2c implementation
# just enough to operate OLED

I2C_SLAVE = 0x0703

class Bus(object):

    def __init__(self, bus):
        self._fd = os.open("/dev/i2c-%d" % bus, os.O_RDWR)
        self._address = -1

    def close(self):
        os.close(self._fd)
        self._address = -1

    def _config_address(self, address):
        if self._address != address:
            ioctl(self._fd, I2C_SLAVE, address)
            self._address = address

    def write(self, address, bytes):
        self._config_address(address)
        return os.write(self._fd, bytes)

