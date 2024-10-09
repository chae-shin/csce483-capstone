import numpy as np
from mido import MidiFile
import time
from rpi_ws281x import PixelStrip, Color

# Constants for LED strip
LED_COUNT      = 300     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to 1 for GPIOs 13, 19, 41, 45 or 53

# Function to convert MIDI file to LED array
def midi_to_led_array(midi_file_path):
    midi = MidiFile(midi_file_path)
    led_array = []

    led_per_tick = 4 / midi.ticks_per_beat  # Number of LEDs per tick (assuming 4 LEDs per beat)

    for track in midi.tracks:
        for msg in track:
            duration_leds = int(msg.time * led_per_tick)  # Number of LEDs for the duration of the event

            if msg.type == 'note_on' and msg.velocity > 0:
                # Note on event
                led_array.extend([(0, 0, 255)] * duration_leds) # Blue for note
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # Note off event or note on with velocity 0 (equivalent to note off)
                led_array.extend([(0, 0, 0)] * duration_leds)  # Off for rest

    return led_array

# Main function
def main():
    # Create NeoPixel object with configuration
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    # Convert MIDI file to LED array
    led_array = midi_to_led_array("output_dummy_note.mid")

    # Iterate through the LED array and update the strip
    for i in range(len(led_array) + LED_COUNT):
        # Shift all LEDs down by one position
        for j in range(LED_COUNT - 1, 0, -1):
            strip.setPixelColor(j, strip.getPixelColor(j - 1))
        
        # Set the first LED to the current color or turn off if past the end of the array
        if i < len(led_array):
            color = Color(*led_array[i])
        else:
            color = Color(0, 0, 0)  # Turn off the LED
        
        strip.setPixelColor(0, color)
        
        # Update the strip
        strip.show()
        
        # Delay to control the speed of the falling effect
        time.sleep(0.1)  # Adjust the delay as needed

if __name__ == "__main__":
    main()