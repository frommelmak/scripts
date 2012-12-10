#!/usr/bin/env python2

# Marcos Martinez
# frommelmak@gmail.com

# Simple script to test the Raspberry Pi GPIO outputs.

import RPi.GPIO as GPIO
from time import sleep
from sys import argv

"""
   GPIO outputs in BCM mode

      | 25 24 23 22 21 18 17  4
   ============================
   2^0|  0  0  0  0  0  0  0  1
   2^1|  0  0  0  0  0  0  1  0 
   2^2|  0  0  0  0  0  1  0  0  
   2^3|  0  0  0  0  1  0  0  0
   2^4|  0  0  0  1  0  0  0  0
   2^5|  0  0  1  0  0  0  0  0
   2^6|  0  1  0  0  0  0  0  0
   2^7|  1  0  0  0  0  0  0  0
"""

def binary_counter(n, speed):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup (25, GPIO.OUT)
    GPIO.setup (24, GPIO.OUT)
    GPIO.setup (23, GPIO.OUT)
    GPIO.setup (22, GPIO.OUT)
    GPIO.setup (21, GPIO.OUT)
    GPIO.setup (18, GPIO.OUT)
    GPIO.setup (17, GPIO.OUT)
    GPIO.setup (4, GPIO.OUT)

    try:
        for n in range(0,n):
            binary = str(bin(n))
            binstr = binary[2:].zfill(8)
            GPIO.output(25, int(binstr[7]))
            GPIO.output(24, int(binstr[6]))
            GPIO.output(23, int(binstr[5]))
            GPIO.output(22, int(binstr[4]))
            GPIO.output(21, int(binstr[3]))
            GPIO.output(18, int(binstr[2]))
            GPIO.output(17, int(binstr[1]))
            GPIO.output(4, int(binstr[0]))
            sleep (speed)
    except:       
        GPIO.cleanup()

    GPIO.cleanup()

if __name__=="__main__":
    DEFAULT_COUNTER=256
    DEFAULT_SPEED=0.2
    try:
      n=int(argv[1])
    except:
      n=DEFAULT_COUNTER
    try:
      speed=float(argv[2])
    except:
      speed=DEFAULT_SPEED
    print "Settings: counter: %d Speed : %f" % (n,speed)
    binary_counter(n, speed)
