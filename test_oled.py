#!/usr/bin/env python

from oled import Adafruit_SSD1306
from i2c import Bus
from RPi import GPIO
import time
import random


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    OLED_RESET = 7
    address = 0x3D
    bus = Bus(0)
    try:
        screen = Adafruit_SSD1306(bus, address, OLED_RESET)

        for n in range(5):
            for i in range(len(screen.buffer)):
                screen.buffer[i] = random.randint(0,255)
            screen.display()
            time.sleep(0.1)

        for i in range(len(screen.buffer)):
            screen.buffer[i] = 0
        
        screen.display()
        time.sleep(0.1)

        for i in range(len(screen.buffer)):
            if i % 8 == 0:
                screen.buffer[i] = 255
            else:
                screen.buffer[i] = 1
        screen.display()
        
    finally:
        GPIO.cleanup()
        bus.close()

