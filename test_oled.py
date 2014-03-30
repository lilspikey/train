from oled import Adafruit_SSD1306
from i2c import Bus
import RPi.GPIO as GPIO


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    OLED_RESET = 4
    address = 0x3D # check this is right
    bus = Bus(1)
    try:
        screen = Adafruit_SSD1306(bus, address, OLED_RESET)
        screen.display()
    finally:
        GPIO.cleanup()
        bus.close()

