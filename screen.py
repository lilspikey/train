#!/usr/bin/env python

from oled import Adafruit_SSD1306
from i2c import Bus
from RPi import GPIO
from PIL import Image, ImageDraw, ImageFont


def get_network_info():
    import socket
    hostname = '{0}.local'.format(socket.gethostname())
    ip = socket.gethostbyname(hostname)
    return hostname, ip


def update_screen(screen):
    image = Image.new('RGB', (screen.WIDTH, screen.HEIGHT))
    d = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    hostname, ip = get_network_info()
    d.text((0,0), hostname, font=font)
    _, ipheight = font.getsize(ip)
    d.text((0, screen.HEIGHT-ipheight), ip, font=font)
    screen.blit(image)


def main():
    GPIO.setmode(GPIO.BOARD)
    OLED_RESET = 7
    address = 0x3D
    bus = Bus(0)
    try:
        screen = Adafruit_SSD1306(bus, address, OLED_RESET)
        update_screen(screen)
    finally:
        GPIO.cleanup()
        bus.close()


if __name__ == '__main__':
    main()
