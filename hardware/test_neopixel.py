# Python test script for the LED Strips
# Author: Rijul Kakar & Chris Avila
# 
# The goal of this script is to test the LED strips
# by turning them on and off in a sequence.

import time
import board
import neopixel

# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels
LED_PIN        = board.D18 # GPIO pin connected to the pixels (18 uses Pulse Width Modulation)
LED_BRIGHTNESS = 1.0      # Brightness of the LEDs (0.0 to 1.0)

# Create NeoPixel object with appropriate configuration.
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)

# Function to turn on the entire LED strip
def turn_on(pixels):
    for i in range(len(pixels)):
        pixels[i] = (255, 0, 0)  # Red color
    pixels.show()

# Function to turn off the entire LED strip
def turn_off(pixels):
    for i in range(len(pixels)):
        pixels[i] = (0, 0, 0)  # Off
    pixels.show()

# Main program logic follows:
if __name__ == '__main__':
    print('Press Ctrl-C to quit.')
    try:
        while True:
            print('Turning on...')
            turn_on(pixels)
            time.sleep(2)
            print('Turning off...')
            turn_off(pixels)
            time.sleep(2)
    except KeyboardInterrupt:
        print('Exiting...')
        turn_off(pixels)