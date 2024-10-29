import numpy as np
from mido import MidiFile
import time
from rpi_ws281x import PixelStrip, Color
import threading

# Constants for LED strip
LED_COUNT      = 100     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to 1 for GPIOs 13, 19, 41, 45 or 53

# Function to convert MIDI file to LED array for a specific note
def midi_to_led_array(midi_file_path, note, color):
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
            if msg.type == 'note_on' and msg.velocity > 0 and msg.note == note:
                if first_note_time is None:
                    first_note_time = current_time
                note_on_times[msg.note] = current_time
                print(f"Note On: {msg}, Current Time: {current_time}")
            elif (msg.type == 'note_off' and msg.note == note) or (msg.type == 'note_on' and msg.velocity == 0 and msg.note == note):
                if msg.note in note_on_times:
                    duration_ticks = current_time - note_on_times[msg.note]
                    duration_leds = int(duration_ticks * led_per_tick)
                    if note_on_times[msg.note] > last_note_end_time:
                        rest_ticks = note_on_times[msg.note] - last_note_end_time
                        rest_leds = int(rest_ticks * led_per_tick)
                        led_array.extend([(0, 0, 0)] * rest_leds)  # Off for rest
                    led_array.extend([color] * duration_leds)  # Color for the note
                    last_note_end_time = current_time
                    print(f"Note Off: {msg}, Duration Ticks: {duration_ticks}, Duration LEDs: {duration_leds}")
                    del note_on_times[msg.note]

    return led_array

# Function to update the left half of the LED strip
def update_left_half(strip, led_array):
    led_strip = [(0, 0, 0)] * (LED_COUNT // 2)
    for i in range(len(led_array) + LED_COUNT // 2):
        for j in range(LED_COUNT // 2 - 1):
            led_strip[j] = led_strip[j + 1]
        if i < len(led_array):
            led_strip[LED_COUNT // 2 - 1] = led_array[i]
        else:
            led_strip[LED_COUNT // 2 - 1] = (0, 0, 0)
        for k in range(LED_COUNT // 2):
            strip.setPixelColor(k, Color(*led_strip[k]))
        strip.show()
        time.sleep(0.1)

# Function to update the right half of the LED strip
def update_right_half(strip, led_array):
    led_strip = [(0, 0, 0)] * (LED_COUNT // 2)
    for i in range(len(led_array) + LED_COUNT // 2):
        for j in range(LED_COUNT // 2 - 1, 0, -1):
            led_strip[j] = led_strip[j - 1]
        if i < len(led_array):
            led_strip[0] = led_array[i]
        else:
            led_strip[0] = (0, 0, 0)
        for k in range(LED_COUNT // 2, LED_COUNT):
            strip.setPixelColor(k, Color(*led_strip[k - LED_COUNT // 2]))
        strip.show()
        time.sleep(0.1)

# Main function
def main():
    # Create NeoPixel object with configuration
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    # Convert MIDI file to LED arrays for A4 and B4
    led_array_a4 = midi_to_led_array("../midi_files/a_4.mid", 69, (0, 0, 255))  # A4 in blue
    led_array_b4 = midi_to_led_array("../midi_files/b4.mid", 71, (255, 0, 0))  # B4 in red

    # Print the LED arrays for debugging
    print("LED Array Length A4:", len(led_array_a4))
    print("LED Array A4:", led_array_a4)
    print("LED Array Length B4:", len(led_array_b4))
    print("LED Array B4:", led_array_b4)

    # Create threads for updating the left and right halves of the LED strip
    left_thread = threading.Thread(target=update_left_half, args=(strip, led_array_a4))
    right_thread = threading.Thread(target=update_right_half, args=(strip, led_array_b4))

    # Start both threads
    left_thread.start()
    right_thread.start()

    # Wait for both threads to finish
    left_thread.join()
    right_thread.join()

if __name__ == "__main__":
    main()