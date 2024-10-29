import numpy as np
from mido import MidiFile
import time
from rpi_ws281x import PixelStrip, Color

# Constants for LED strip
LED_COUNT      = 100     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to 1 for GPIOs 13, 19, 41, 45 or 53

# Function to convert MIDI file to LED array for A4 note
def midi_to_led_array(midi_file_path):
    midi = MidiFile(midi_file_path)
    led_array = []

    led_per_tick = 4 / midi.ticks_per_beat  # Number of LEDs per tick (assuming 4 LEDs per beat)
    note_on_times = {}  # Dictionary to track note_on times

    first_note_time = None
    last_note_end_time = 0

    for track in midi.tracks:
        current_time = 0
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0 and msg.note == 69:  # A4
                if first_note_time is None:
                    first_note_time = current_time
                note_on_times[msg.note] = current_time
                print(f"Note On: {msg}, Current Time: {current_time}")
            elif (msg.type == 'note_off' and msg.note == 69) or (msg.type == 'note_on' and msg.velocity == 0 and msg.note == 69):
                if msg.note in note_on_times:
                    duration_ticks = current_time - note_on_times[msg.note]
                    duration_leds = int(duration_ticks * led_per_tick)
                    if note_on_times[msg.note] > last_note_end_time:
                        rest_ticks = note_on_times[msg.note] - last_note_end_time
                        rest_leds = int(rest_ticks * led_per_tick)
                        led_array.extend([(0, 0, 0)] * rest_leds)  # Off for rest
                    led_array.extend([(0, 0, 255)] * duration_leds)  # Blue for A4
                    last_note_end_time = current_time
                    print(f"Note Off: {msg}, Duration Ticks: {duration_ticks}, Duration LEDs: {duration_leds}")
                    del note_on_times[msg.note]

    if first_note_time is not None:
        initial_rest_ticks = first_note_time
        initial_rest_leds = int(initial_rest_ticks * led_per_tick)
        led_array = [(0, 0, 0)] * initial_rest_leds + led_array  # Add initial rest

    return led_array

# Main function
def main():
    # Create NeoPixel object with configuration
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    # Convert MIDI file to LED array
    led_array = midi_to_led_array("../midi_files/a4_bizarre.mid")

    # Print the LED array for debugging
    print("LED Array Length:", len(led_array))
    print("LED Array:", led_array)

    # Initialize LED strip as a list of off colors
    led_strip = [(0, 0, 0)] * LED_COUNT

    # Iterate through the LED array and update the strip
    for i in range(len(led_array) + LED_COUNT):
        # Shift all LEDs down by one position
        for j in range(LED_COUNT - 1, 0, -1):
            led_strip[j] = led_strip[j - 1]

        # Set the first LED to the current color
        if i < len(led_array):
            led_strip[0] = led_array[i]
        else:
            led_strip[0] = (0, 0, 0)  # Turn off the LED

        # Update the physical LED strip
        for k in range(LED_COUNT):
            strip.setPixelColor(k, Color(*led_strip[k]))
        strip.show()

        # Delay to control the speed of the falling effect
        time.sleep(0.1)  # Adjust the delay as needed

if __name__ == "__main__":
    main()