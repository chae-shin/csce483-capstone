import numpy as np
from mido import MidiFile
import time
from rpi_ws281x import PixelStrip, Color
import threading

# Constants for LED strip
LED_COUNT      = 200     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to 1 for GPIOs 13, 19, 41, 45 or 53

# Function to convert a single MIDI file to LED arrays for specified notes
def midi_to_led_arrays(midi_file_path, notes, colors):
    midi = MidiFile(midi_file_path)
    led_arrays = {note: [] for note in notes}
    note_on_times = {note: [] for note in notes}
    last_note_end_times = {note: 0 for note in notes}
    
    led_per_tick = 4 / midi.ticks_per_beat  # Number of LEDs per tick (assuming 4 LEDs per beat)
    first_note_time = None  # For overall time alignment, if needed

    for track in midi.tracks:
        current_time = 0
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0 and msg.note in notes:
                if first_note_time is None:
                    first_note_time = current_time
                note_on_times[msg.note].append(current_time)
                print(f"Note On: {msg}, Current Time: {current_time}")
            elif ((msg.type == 'note_off' and msg.note in notes) or 
                  (msg.type == 'note_on' and msg.velocity == 0 and msg.note in notes)):
                if note_on_times[msg.note]:
                    note_on_time = note_on_times[msg.note].pop(0)
                    duration_ticks = current_time - note_on_time
                    duration_leds = int(duration_ticks * led_per_tick)
                    # Handle rest before note
                    if note_on_time > last_note_end_times[msg.note]:
                        rest_ticks = note_on_time - last_note_end_times[msg.note]
                        rest_leds = int(rest_ticks * led_per_tick)
                        led_arrays[msg.note].extend([(0, 0, 0)] * rest_leds)
                    led_arrays[msg.note].extend([colors[notes.index(msg.note)]] * duration_leds)
                    last_note_end_times[msg.note] = current_time
                    print(f"Note Off: {msg}, Duration Ticks: {duration_ticks}, Duration LEDs: {duration_leds}")
                else:
                    print(f"Note Off without Note On: {msg}, Current Time: {current_time}")

    return led_arrays

# Functions to update each quarter of the LED strip
def update_first_quarter(strip, led_array):
    led_strip = [(0, 0, 0)] * (LED_COUNT // 4)
    for i in range(len(led_array) + LED_COUNT // 4):
        for j in range(LED_COUNT // 4 - 1):
            led_strip[j] = led_strip[j + 1]
        if i < len(led_array):
            led_strip[LED_COUNT // 4 - 1] = led_array[i]
        else:
            led_strip[LED_COUNT // 4 - 1] = (0, 0, 0)
        for k in range(LED_COUNT // 4):
            strip.setPixelColor(k, Color(*led_strip[k]))
        strip.show()
        time.sleep(0.1)

def update_second_quarter(strip, led_array):
    led_strip = [(0, 0, 0)] * (LED_COUNT // 4)
    for i in range(len(led_array) + LED_COUNT // 4):
        for j in range(LED_COUNT // 4 - 1, 0, -1):
            led_strip[j] = led_strip[j - 1]
        if i < len(led_array):
            led_strip[0] = led_array[i]
        else:
            led_strip[0] = (0, 0, 0)
        for k in range(LED_COUNT // 4, LED_COUNT // 2):
            strip.setPixelColor(k, Color(*led_strip[k - LED_COUNT // 4]))
        strip.show()
        time.sleep(0.1)

def update_third_quarter(strip, led_array):
    led_strip = [(0, 0, 0)] * (LED_COUNT // 4)
    for i in range(len(led_array) + LED_COUNT // 4):
        for j in range(LED_COUNT // 4 - 1):
            led_strip[j] = led_strip[j + 1]
        if i < len(led_array):
            led_strip[LED_COUNT // 4 - 1] = led_array[i]
        else:
            led_strip[LED_COUNT // 4 - 1] = (0, 0, 0)
        for k in range(LED_COUNT // 2, 3 * LED_COUNT // 4):
            strip.setPixelColor(k, Color(*led_strip[k - LED_COUNT // 2]))
        strip.show()
        time.sleep(0.1)

def update_fourth_quarter(strip, led_array):
    led_strip = [(0, 0, 0)] * (LED_COUNT // 4)
    for i in range(len(led_array) + LED_COUNT // 4):
        for j in range(LED_COUNT // 4 - 1, 0, -1):
            led_strip[j] = led_strip[j - 1]
        if i < len(led_array):
            led_strip[0] = led_array[i]
        else:
            led_strip[0] = (0, 0, 0)
        for k in range(3 * LED_COUNT // 4, LED_COUNT):
            strip.setPixelColor(k, Color(*led_strip[k - 3 * LED_COUNT // 4]))
        strip.show()
        time.sleep(0.1)

# Main function
def main():
    # Create NeoPixel object with configuration
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    
    # Define notes and colors
    notes = [69, 71, 72, 74]  # A4, B4, C5, D5
    colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0)]  # Blue, Red, Green, Yellow
    
    # Convert MIDI file to LED arrays for the notes
    led_arrays = midi_to_led_arrays("../midi_files/chris_test_4_notes3.mid", notes, colors)
    
    # Print the LED arrays for debugging
    for note in notes:
        print(f"LED Array Length for Note {note}:", len(led_arrays[note]))
        print(f"LED Array for Note {note}:", led_arrays[note])
    
    # Create threads for updating the quarters of the LED strip
    first_thread = threading.Thread(target=update_first_quarter, args=(strip, led_arrays[69]))
    second_thread = threading.Thread(target=update_second_quarter, args=(strip, led_arrays[71]))
    third_thread = threading.Thread(target=update_third_quarter, args=(strip, led_arrays[72]))
    fourth_thread = threading.Thread(target=update_fourth_quarter, args=(strip, led_arrays[74]))
    
    # Start all threads
    first_thread.start()
    second_thread.start()
    third_thread.start()
    fourth_thread.start()
    
    # Wait for all threads to finish
    first_thread.join()
    second_thread.join()
    third_thread.join()
    fourth_thread.join()

if __name__ == "__main__":
    main()
