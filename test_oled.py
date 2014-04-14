#!/usr/bin/env python

from oled import Adafruit_SSD1306
from i2c import Bus
from RPi import GPIO
import time
import pygame.image
import pygame.transform
import sys


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    OLED_RESET = 7
    address = 0x3D
    bus = Bus(0)
    try:
        screen = Adafruit_SSD1306(bus, address, OLED_RESET)
        
        for name in sys.argv[1:]:
            surface = pygame.image.load(name)
            scaled = pygame.transform.smoothscale(surface, (screen.WIDTH, screen.HEIGHT))
            screen.blit(scaled)
            time.sleep(1)
        
    finally:
        GPIO.cleanup()
        bus.close()

