import numpy as np
from mido import MidiFile
import time
from rpi_ws281x import PixelStrip, Color

# Constants for LED strip
LED_COUNT      = 500     # Total number of LEDs (10 notes * 50 LEDs per note)
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # Set to 1 for GPIOs 13, 19, 41, 45 or 53

# Function to convert a single MIDI file to LED arrays for specified notes
def midi_to_led_arrays(midi_file_path, notes, colors, alt_colors):
    midi = MidiFile(midi_file_path)
    led_arrays = {note: [] for note in notes}
    note_on_times = {note: [] for note in notes}
    last_note_end_times = {note: 0 for note in notes}
    consecutive_note_counts = {note: -1 for note in notes}  # Start at -1 for correct alternation

    led_per_tick = 4 / midi.ticks_per_beat  # Number of LEDs per tick (assuming 4 LEDs per beat)
    rest_threshold_ticks = midi.ticks_per_beat * 0.05  # Adjust the threshold as needed (e.g., 5% of a beat)

    for track in midi.tracks:
        current_time = 0
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0 and msg.note in notes:
                note_on_times[msg.note].append(current_time)
                print(f"Note On: {msg}, Current Time: {current_time}")
            elif ((msg.type == 'note_off' and msg.note in notes) or
                  (msg.type == 'note_on' and msg.velocity == 0 and msg.note in notes)):
                if note_on_times[msg.note]:
                    note_on_time = note_on_times[msg.note].pop(0)
                    duration_ticks = current_time - note_on_time
                    duration_leds = int(duration_ticks * led_per_tick)

                    # Determine if there was a significant rest before this note
                    gap_ticks = note_on_time - last_note_end_times[msg.note]
                    if gap_ticks > rest_threshold_ticks:
                        # There was a rest, reset consecutive note count
                        rest_leds = int(gap_ticks * led_per_tick)
                        led_arrays[msg.note].extend([(0, 0, 0)] * rest_leds)
                        consecutive_note_counts[msg.note] = -1  # Start at -1 to use base color first
                    else:
                        # No significant rest
                        # If there is a small gap, fill it without resetting the count
                        if gap_ticks > 0:
                            gap_leds = int(gap_ticks * led_per_tick)
                            led_arrays[msg.note].extend([(0, 0, 0)] * gap_leds)

                    # Increment the consecutive note count
                    consecutive_note_counts[msg.note] += 1

                    # Alternate color for consecutive notes
                    note_index = notes.index(msg.note)
                    base_color = colors[note_index]
                    alternate_color = alt_colors[note_index]
                    if consecutive_note_counts[msg.note] % 2 == 0:
                        # Use base color on even counts
                        used_color = base_color
                    else:
                        # Use alternate (darker) color on odd counts
                        used_color = alternate_color

                    led_arrays[msg.note].extend([used_color] * duration_leds)
                    last_note_end_times[msg.note] = current_time
                    print(f"Note Off: {msg}, Duration Ticks: {duration_ticks}, Duration LEDs: {duration_leds}")
                else:
                    print(f"Note Off without Note On: {msg}, Current Time: {current_time}")

    return led_arrays

# Main function
def main():
    # Create NeoPixel object with configuration
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    # Define notes for C1 to A1 (10 notes)
    notes = list(range(24, 34))  # MIDI notes from C1 (24) to A1 (33)

    # Identify white and black keys
    white_keys = [24, 26, 28, 29, 31, 33]
    black_keys = [25, 27, 30, 32]

    colors = []
    alt_colors = []

    for note in notes:
        if note in white_keys:
            colors.append((255, 0, 0))      # Base red for white keys
            alt_colors.append((0, 0, 255))  # Blue for alternation
        elif note in black_keys:
            colors.append((128, 0, 128))    # Base purple for black keys
            alt_colors.append((0, 255, 0))  # Green for alternation
        else:
            colors.append((0, 0, 0))        # Default to black if note is not identified
            alt_colors.append((0, 0, 0))

    # Print colors for debugging
    print("Colors:", colors)
    print("Alt Colors:", alt_colors)

    # Convert MIDI file to LED arrays for the notes
    midi_file_path = "../midi_files/hot_cross_buns.mid"  # Replace with your MIDI file path
    led_arrays = midi_to_led_arrays(midi_file_path, notes, colors, alt_colors)

    # Print the LED arrays for debugging
    for note in notes:
        print(f"LED Array Length for Note {note}:", len(led_arrays[note]))
        # Uncomment the next line if you want to print the entire array (can be long)
        # print(f"LED Array for Note {note}:", led_arrays[note])

    # Each note gets 50 LEDs
    leds_per_note = 50
    total_leds_needed = leds_per_note * len(notes)
    if total_leds_needed > LED_COUNT:
        print(f"Error: Not enough LEDs. Required: {total_leds_needed}, Available: {LED_COUNT}")
        return

    # Prepare led_strips
    led_strips = {}
    for idx, note in enumerate(notes):
        led_strips[note] = [(0, 0, 0)] * leds_per_note

    # Find the maximum length among all led_arrays
    max_length = max(len(led_arrays[note]) for note in notes) + leds_per_note

    frame_duration = 0.1  # Desired frame duration in seconds

    for i in range(max_length):
        start_time = time.time()
        for idx, note in enumerate(notes):
            start_index = idx * leds_per_note
            end_index = start_index + leds_per_note
            section_length = leds_per_note
            led_strip = led_strips[note]
            led_array = led_arrays[note]

            # Shift and update led_strip for each note
            if idx % 2 == 0:
                # Left shift
                for j in range(section_length - 1):
                    led_strip[j] = led_strip[j + 1]
                if i < len(led_array):
                    led_strip[section_length - 1] = led_array[i]
                else:
                    led_strip[section_length - 1] = (0, 0, 0)
            else:
                # Right shift
                for j in range(section_length - 1, 0, -1):
                    led_strip[j] = led_strip[j - 1]
                if i < len(led_array):
                    led_strip[0] = led_array[i]
                else:
                    led_strip[0] = (0, 0, 0)
            led_strips[note] = led_strip

            # Update the strip for this section
            for k in range(section_length):
                strip.setPixelColor(start_index + k, Color(*led_strip[k]))

        # After updating all sections, show the strip
        strip.show()

        # Calculate elapsed time and sleep to maintain frame rate
        elapsed_time = time.time() - start_time
        time_to_sleep = frame_duration - elapsed_time
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    # Clear the strip at the end
    clear_strip(strip)

def clear_strip(strip):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

if __name__ == "__main__":
    main()
