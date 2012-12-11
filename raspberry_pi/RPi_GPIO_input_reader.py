#!/usr/bin/env python2

# Marcos Martinez
# frommelmak@gmail.com

# Simple script to test the Raspberry Pi GPIO inputs.

import RPi.GPIO as GPIO

"""
   GPIO secure inputs diagram

           ^ 3.3V
           |
           |
           |
            /  10K
   switch  /   ___
           |--|___|--
           |        |
           |       --- GND
         [pin]      -  
          GPIO
"""

def read_input(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    value = GPIO.input(pin)
    return value

if __name__=="__main__":
    pins = [4,17,18,21,22,23,24,25]
    for pin in pins:
      value = read_input (pin)
      print "Value of pin %d: %d" % (pin, value)
