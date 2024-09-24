# Python test script for the LED Strips
# Author: Rijul Kakar & Chris Avila
# 
# The goal of this script is to test the LED strips
# by turning them on and off in a sequence.


import time
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses Pulse Width Modulation)
# If we want to use SPI, we can use the pin 10
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to 1 for GPIOs 13, 19, 41, 45 or 53

# Function to turn on the entire LED strip
def turn_on(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 255, 0)) # Green
    strip.show()

# Function to turn off the entire LED strip
def turn_off(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0)) # Off
    strip.show()

# Function to turn LEDs on one by one (previous one turns off)
def turn_on_one_by_one(strip):
    for i in range(strip.numPixels()):
        if i > 0:
            strip.setPixelColor(i-1, Color(0, 0, 0)) # Off
        strip.setPixelColor(i, Color(0, 255, 255)) # Cyan
