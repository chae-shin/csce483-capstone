import time
from rpi_ws281x import *
import argparse
import queue
import mido

# LED strip configuration:
LED_COUNT = 60      # Number of LED pixels
LED_PIN = 18        # GPIO pin connected to the pixels (18 uses PWM!)
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10        # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0     # set to 1 for GPIOs 13, 19, 41, 45 or 53

# MIDI note number for A4
NOTE_A4 = 69

# LED colors
PURPLE = (128, 0, 128)
RED = (0, 0, 0)  # Rest is now black

# Number of LEDs for each note/rest
LEDS_PER_NOTE = 8

# Initialize the queue
q = queue.Queue()

def parse_midi_file(file_path):
    midi_file = mido.MidiFile(file_path)
    note_on = False
    led_pattern = []
    
    for msg in midi_file:
        if msg.type == 'note_on' and msg.note == NOTE_A4 and msg.velocity > 0:
            q.put([PURPLE] * LEDS_PER_NOTE)
            note_on = True
        elif (msg.type == 'note_off' and msg.note == NOTE_A4) or \
             (msg.type == 'note_on' and msg.note == NOTE_A4 and msg.velocity == 0):
            q.put([RED] * LEDS_PER_NOTE)
            note_on = False
    
    # Collect all commands from the queue
    while not q.empty():
        led_pattern.extend(q.get())
    
    # Add 6 rest notes at the end
    led_pattern.extend([RED] * (LEDS_PER_NOTE * 6))
    
    return led_pattern

def display_led_pattern(strip, led_pattern):
    for color in led_pattern:
        # Shift all LEDs down by one position
        for j in range(LED_COUNT - 1, 0, -1):
            strip.setPixelColor(j, strip.getPixelColor(j - 1))
        
        # Set the first LED to the current color
        strip.setPixelColor(0, Color(*color))
        
        # Update the strip
        strip.show()
        
        # Delay to control the speed of the falling effect
        time.sleep(0.1)  # Adjust the delay as needed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-f', '--file', required=True, help='MIDI file to process')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    try:
        # Parse MIDI file
        led_pattern = parse_midi_file(args.file)
        
        # Display LED pattern with falling effect
        display_led_pattern(strip, led_pattern)

    except KeyboardInterrupt:
        if args.clear:
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()

if __name__ == '__main__':
    main()

