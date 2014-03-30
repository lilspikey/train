import struct
import GPIO
import time
from array import array

# porting over from https://github.com/adafruit/Adafruit_SSD1306/blob/master/Adafruit_SSD1306.cpp

SSD1306_SETCONTRAST=0x81
SSD1306_DISPLAYALLON_RESUME=0xA4
SSD1306_DISPLAYALLON=0xA5
SSD1306_NORMALDISPLAY=0xA6
SSD1306_INVERTDISPLAY=0xA7
SSD1306_DISPLAYOFF=0xAE
SSD1306_DISPLAYON=0xAF

SSD1306_SETDISPLAYOFFSET=0xD3
SSD1306_SETCOMPINS=0xDA

SSD1306_SETVCOMDETECT=0xDB

SSD1306_SETDISPLAYCLOCKDIV=0xD5
SSD1306_SETPRECHARGE=0xD9

SSD1306_SETMULTIPLEX=0xA8

SSD1306_SETLOWCOLUMN=0x00
SSD1306_SETHIGHCOLUMN=0x10

SSD1306_SETSTARTLINE=0x40

SSD1306_MEMORYMODE=0x20
SSD1306_COLUMNADDR=0x21
SSD1306_PAGEADDR=0x22

SSD1306_COMSCANINC=0xC0
SSD1306_COMSCANDEC=0xC8

SSD1306_SEGREMAP=0xA0

SSD1306_CHARGEPUMP=0x8D

SSD1306_EXTERNALVCC=0x1
SSD1306_SWITCHCAPVCC=0x2

SSD1306_ACTIVATE_SCROLL=0x2F
SSD1306_DEACTIVATE_SCROLL=0x2E
SSD1306_SET_VERTICAL_SCROLL_AREA=0xA3
SSD1306_RIGHT_HORIZONTAL_SCROLL=0x26
SSD1306_LEFT_HORIZONTAL_SCROLL=0x27
SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL=0x29
SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL=0x2A



class Adafruit_SSD1306(object):
    WIDTH = 128
    HEIGHT = 64

    def __init__(self, bus, address, reset_pin, vccstate=SSD1306_SWITCHCAPVCC):
        self.bus = bus
        self.address = address
        self.buffer = array('B', [0 for i in range(self.WIDTH*self.HEIGHT/8)])

        GPIO.setup(reset_pin, GPIO.OUT)
        GPIO.output(reset_pin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(reset_pin, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(reset_pin, GPIO.HIGH)

        self.ssd1306_command(SSD1306_DISPLAYOFF)
        self.ssd1306_command(SSD1306_SETDISPLAYCLOCKDIV)
        self.ssd1306_command(0x80)
        self.ssd1306_command(SSD1306_SETMULTIPLEX)
        self.ssd1306_command(0x3F)
        self.ssd1306_command(SSD1306_SETDISPLAYOFFSET)
        self.ssd1306_command(0x0)
        self.ssd1306_command(SSD1306_SETSTARTLINE | 0x0)
        self.ssd1306_command(SSD1306_CHARGEPUMP)
        if vccstate == SSD1306_EXTERNALVCC:
            self.ssd1306_command(0x10)
        else:
            self.ssd1306_command(0x14)
        self.ssd1306_command(SSD1306_MEMORYMODE)
        self.ssd1306_command(0x00)
        self.ssd1306_command(SSD1306_SEGREMAP | 0x1)
        self.ssd1306_command(SSD1306_COMSCANDEC)
        self.ssd1306_command(SSD1306_SETCOMPINS)
        self.ssd1306_command(0x12)
        self.ssd1306_command(SSD1306_SETCONTRAST)
        if :vccstate == SSD1306_EXTERNALVCC:
            self.ssd1306_command(0x9F)
        else: 
            self.ssd1306_command(0xCF)
        self.ssd1306_command(SSD1306_SETPRECHARGE)
        if vccstate == SSD1306_EXTERNALVCC:
            self.ssd1306_command(0x22)
        else:
            self.ssd1306_command(0xF1)
        self.ssd1306_command(SSD1306_SETVCOMDETECT)
        self.ssd1306_command(0x40)
        self.ssd1306_command(SSD1306_DISPLAYALLON_RESUME)
        self.ssd1306_command(SSD1306_NORMALDISPLAY)
        self.ssd1306_command(SSD1306_DISPLAYON)
    
    def ssd1306_command(self, cmd):
        bytes = struct.pack('BB', 0, cmd)
        self.bus.write(self.address, bytes)

    def ssd1306_data(self, bytes):
        bytes = struct.pack('B%dB' % len(bytes), *bytes)
        self.bus.write(self.address, bytes)

    def display(self):
        self.ssd1306_command(SSD1306_COLUMNADDR)
        self.ssd1306_command(0)
        ssd1306_command(127)

        ssd1306_command(SSD1306_PAGEADDR)
        ssd1306_command(0)
        ssd1306_command(7)

        for i in xrange(0, len(self.buffer), 16):
            data = self.buffer[i:i+16]
            self.ssd1306_data(data)
        
