#!/usr/bin/env python

'''
simple script to listen out for changes in GPIO port that show that
power button pressed and we should shutdown RPi
'''

import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BOARD)

SHUTDOWN_REQUEST_PIN = 16
SHUTDOWN_CONFIRM_PIN = 18

try:
    GPIO.setup(SHUTDOWN_REQUEST_PIN, GPIO.IN)
    
    GPIO.setup(SHUTDOWN_CONFIRM_PIN, GPIO.OUT, initial=GPIO.HIGH)

    while GPIO.input(SHUTDOWN_REQUEST_PIN) == GPIO.HIGH:
        time.sleep(0.25)

    # used for debug purposes
    #print("SHUTDOWN")
    #GPIO.output(SHUTDOWN_CONFIRM_PIN, GPIO.LOW)

    subprocess.call('halt', shell=False)
finally:
    # only cleanup request pin, as we want confirm pin to stay high
    # until RPi has actually shutdown
    GPIO.cleanup(SHUTDOWN_REQUEST_PIN)


