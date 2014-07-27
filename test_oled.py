#!/usr/bin/env python

from oled import Adafruit_SSD1306
from i2c import Bus
from RPi import GPIO
import time
from PIL import Image
import sys


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    OLED_RESET = 7
    address = 0x3D
    bus = Bus(0)
    try:
        screen = Adafruit_SSD1306(bus, address, OLED_RESET)
        
        for name in sys.argv[1:]:
            image = Image.open(name)
            image = image.resize((screen.WIDTH, screen.HEIGHT))
            image = image.convert('RGB')
            screen.blit(image)
            time.sleep(1)
        
    finally:
        GPIO.cleanup()
        bus.close()

