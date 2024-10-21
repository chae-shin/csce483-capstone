import numpy as np
from mido import MidiFile
import time
from rpi_ws281x import PixelStrip, Color

# Constants for LED strip
LED_COUNT      = 60     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to 1 for GPIOs 13, 19, 41, 45 or 53

# MIDI note numbers for A4 and B4
A4_NOTE = 69
B4_NOTE = 71

# Function to convert MIDI file to LED array
def midi_to_led_array(midi_file_path):
    midi = MidiFile(midi_file_path)
    led_array_left = []
    led_array_right = []

    led_per_tick = 4 / midi.ticks_per_beat  # Number of LEDs per tick (assuming 16 LEDs per whole note)
    current_time = 0  # Current time to track the total time elapsed

    for track in midi.tracks:
        for msg in track:
            if msg.time > 0:
                current_time = msg.time
            duration_leds = int(current_time * led_per_tick)  # Number of LEDs for the duration of the event

            if msg.type == 'note_on' and msg.velocity > 0:
                if msg.note == A4_NOTE:
                    # Note A4 event - Left half
                    print(f"Detected A4 note: {msg.note}, Time: {msg.time}, Duration LEDs: {duration_leds}")
                    led_array_left.extend([(0, 0, 255)] * duration_leds)  # Blue for note A4
                elif msg.note == B4_NOTE:
                    # Note B4 event - Right half
                    print(f"Detected B4 note: {msg.note}, Time: {msg.time}, Duration LEDs: {duration_leds}")
                    led_array_right.extend([(255, 0, 0)] * duration_leds)  # Red for note B4
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # Note off event or note on with velocity 0 (equivalent to note off)
                if msg.note == A4_NOTE:
                    led_array_left.extend([(0, 0, 0)] * duration_leds)  # Off for rest
                elif msg.note == B4_NOTE:
                    led_array_right.extend([(0, 0, 0)] * duration_leds)  # Off for rest

    print("LED Array Left:", led_array_left)
    print("LED Array Right:", led_array_right)

    return led_array_left, led_array_right

# Main function
def main():
    # Create NeoPixel object with configuration
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    # Convert MIDI file to LED arrays for both notes
    led_array_left, led_array_right = midi_to_led_array("output_two_notes.mid")

    # Iterate through the LED arrays and update the strip
    max_len = max(len(led_array_left), len(led_array_right))
    for i in range(max_len + LED_COUNT):
        # Shift all LEDs up by one position for the left half (A4)
        for j in range(LED_COUNT // 2 - 1):
            strip.setPixelColor(j, strip.getPixelColor(j + 1))

        # Shift all LEDs down by one position for the right half (B4)
        for j in range(LED_COUNT - 1, LED_COUNT // 2, -1):
            strip.setPixelColor(j, strip.getPixelColor(j - 1))

        # Set the last LED on each half to the current color or turn off if past the end of the array
        if i < len(led_array_left):
            color_left = Color(*led_array_left[i])
        else:
            color_left = Color(0, 0, 0)  # Turn off the LED
        
        if i < len(led_array_right):
            color_right = Color(*led_array_right[i])
        else:
            color_right = Color(0, 0, 0)  # Turn off the LED

        strip.setPixelColor(LED_COUNT // 2 - 1, color_left)
        strip.setPixelColor(LED_COUNT // 2, color_right)

        # Update the strip
        strip.show()
        
        # Delay to control the speed of the falling effect
        time.sleep(0.1)  # Adjust the delay as needed

if __name__ == "__main__":
    main()