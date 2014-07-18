#!/usr/bin/env python

'''
simple script to listen out for changes in GPIO port that show that
power button pressed and we should shutdown RPi
'''

import RPi.GPIO as GPIO


SHUTDOWN_REQUEST_PIN = 16
SHUTDOWN_CONFIRM_PIN = 18


def start(debug=False):
    import time
    import subprocess

    GPIO.output(SHUTDOWN_CONFIRM_PIN, GPIO.HIGH)

    while GPIO.input(SHUTDOWN_REQUEST_PIN) == GPIO.HIGH:
        time.sleep(0.25)
    
    if debug:
        print("SHUTDOWN")
    else:
        subprocess.call('poweroff', shell=False)
    GPIO.output(SHUTDOWN_CONFIRM_PIN, GPIO.LOW)


def main(args):
    GPIO.setmode(GPIO.BOARD)
    
    try:
        GPIO.setup(SHUTDOWN_REQUEST_PIN, GPIO.IN)
        GPIO.setup(SHUTDOWN_CONFIRM_PIN, GPIO.OUT)
        
        start(args.debug)

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Deals with power on/off button')
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()
    main(args)

