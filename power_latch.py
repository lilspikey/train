#!/usr/bin/env python

'''
simple script to listen out for changes in GPIO port that show that
power button pressed and we should shutdown RPi
'''

import RPi.GPIO as GPIO


SHUTDOWN_REQUEST_PIN = 16
SHUTDOWN_CONFIRM_PIN = 18


def is_shutdown_requested():
    if GPIO.input(SHUTDOWN_REQUEST_PIN) == GPIO.HIGH:
        time.sleep(0.05)
        return GPIO.input(SHUTDOWN_REQUEST_PIN) == GPIO.HIGH
    return False


def start(debug=False):
    import time
    import subprocess

    # low means we don't want to power down
    GPIO.output(SHUTDOWN_CONFIRM_PIN, GPIO.LOW)

    while not is_shutdown_requested():
        time.sleep(0.1)
    
    if debug:
        print("SHUTDOWN")
        GPIO.setup(SHUTDOWN_CONFIRM_PIN, GPIO.IN)
    else:
        subprocess.call('poweroff', shell=False)


def main(args):
    GPIO.setmode(GPIO.BOARD)
    
    try:
        GPIO.setup(SHUTDOWN_REQUEST_PIN, GPIO.IN)
        GPIO.setup(SHUTDOWN_CONFIRM_PIN, GPIO.OUT)
        
        start(args.debug)

    finally:
        # just clean this pin, as we'll rely
        # on confirm pin getting switched to input
        # when RPi powers down (which should pull
        # things high on level converter)
        GPIO.cleanup(SHUTDOWN_REQUEST_PIN)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Deals with power on/off button')
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()
    main(args)

