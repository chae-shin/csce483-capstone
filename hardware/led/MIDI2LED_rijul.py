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
                led_array.extend([(0, 0, 0)] * duration_leds)  # Blue for note
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # Note off event or note on with velocity 0 (equivalent to note off)
                led_array.extend([(0, 0, 255)] * duration_leds)  # Off for rest

    return led_array





# Main function -- right side of the led strip for one of the notes
def main():
    # Create NeoPixel object with configuration
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    # Convert MIDI file to LED array
    led_array = midi_to_led_array("output_two_notes.mid")

    # Iterate through the LED array and update the strip
    for i in range(len(led_array) + LED_COUNT):
        # Shift all LEDs down by one position starting from LED 30
        for j in range(LED_COUNT - 1, 0, -1):  # Start from the last LED
            strip.setPixelColor(j, strip.getPixelColor(j - 1))
        
        # Set the starting position to 30
        if i < len(led_array):
            color = Color(*led_array[i])
        else:
            color = Color(0, 0, 0)  # Turn off the LED
        
        # Set the 30th LED (index 29) to the current color
        if i < len(led_array) + 30:
            strip.setPixelColor(29, color)  # Set the 30th LED
        
        # Update the strip
        strip.show()
        
        # Delay to control the speed of the falling effect
        time.sleep(0.1)  # Adjust the delay as needed

if __name__ == "__main__":
    main()

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

# Function to convert MIDI file to LED arrays for two notes
def midi_to_led_arrays(midi_file_path):
    midi = MidiFile(midi_file_path)
    led_a4_array = []
    led_b4_array = []

    led_per_tick = 4 / midi.ticks_per_beat  # Number of LEDs per tick (assuming 4 LEDs per beat)

    for track in midi.tracks:
        for msg in track:
            duration_leds = int(msg.time * led_per_tick)  # Number of LEDs for the duration of the event
            
            if msg.type == 'note_on' and msg.velocity > 0:
                if msg.note == 69:  # A4
                    led_a4_array.extend([(0, 0, 255)] * duration_leds)  # Blue for A4
                elif msg.note == 71:  # B4
                    led_b4_array.extend([(255, 0, 0)] * duration_leds)  # Red for B4
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note == 69:
                    led_a4_array.extend([(0, 0, 0)] * duration_leds)  # Off for A4
                elif msg.note == 71:
                    led_b4_array.extend([(0, 0, 0)] * duration_leds)  # Off for B4

    return led_a4_array, led_b4_array

# Main function -- right side of the LED strip for both notes
def main():
    # Create NeoPixel object with configuration
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    # Convert MIDI file to LED arrays
    led_a4_array, led_b4_array = midi_to_led_arrays("output_two_notes.mid")

    max_length = max(len(led_a4_array), len(led_b4_array))

    # Debug: Print lengths of LED arrays
    print(f"Length of A4 LED array: {len(led_a4_array)}")
    print(f"Length of B4 LED array: {len(led_b4_array)}")

    # Iterate through the maximum length of both LED arrays
    for i in range(max_length + LED_COUNT):
        # Shift all LEDs down by one position starting from LED 31 for A4
        for j in range(LED_COUNT - 1, 31, -1):  # Start from the last LED
            strip.setPixelColor(j, strip.getPixelColor(j - 1))
        
        # Shift all LEDs up by one position starting from LED 30 for B4
        for j in range(30, 0, -1):  # Start from LED 30 to 0
            strip.setPixelColor(j, strip.getPixelColor(j - 1))
        
        # Set the 31st LED (index 30) to the current color for A4
        if i < len(led_a4_array):
            color_a4 = Color(*led_a4_array[i])
        else:
            color_a4 = Color(0, 0, 0)  # Turn off the LED
        
        strip.setPixelColor(31, color_a4)  # Set the 31st LED for A4
        
        # Debug: Print current color for A4
        print(f"Step {i}: A4 Color - {color_a4}")

        # Set the 30th LED (index 29) to the current color for B4
        if i < len(led_b4_array):
            color_b4 = Color(*led_b4_array[i])
        else:
            color_b4 = Color(0, 0, 0)  # Turn off the LED
        
        strip.setPixelColor(30, color_b4)  # Set the 30th LED for B4
        
        # Debug: Print current color for B4
        print(f"Step {i}: B4 Color - {color_b4}")

        # Update the strip
        strip.show()
        
        # Delay to control the speed of the falling effect
        time.sleep(0.1)  # Adjust the delay as needed

if __name__ == "__main__":
    main()

# import numpy as np
# from mido import MidiFile
# import time
# from rpi_ws281x import PixelStrip, Color

# # Constants for LED strip
# LED_COUNT      = 60     # Number of LED pixels.
# LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
# LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
# LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL    = 0       # set to 1 for GPIOs 13, 19, 41, 45 or 53

# # Function to convert MIDI file to LED arrays for two notes
# def midi_to_led_arrays(midi_file_path):
#     midi = MidiFile(midi_file_path)
#     led_a4_array = []
#     led_b4_array = []

#     led_per_tick = 4 / midi.ticks_per_beat  # Number of LEDs per tick (assuming 4 LEDs per beat)

#     for track in midi.tracks:
#         for msg in track:
#             print(f"Message: {msg}")  # Print the MIDI message for debugging
#             duration_leds = int(msg.time * led_per_tick)  # Number of LEDs for the duration of the event

#             if msg.type == 'note_on' and msg.velocity > 0:
#                 if msg.note == 69:  # A4
#                     led_a4_array.extend([(0, 0, 255)] * duration_leds)  # Blue for A4
#                 elif msg.note == 71:  # B4
#                     led_b4_array.extend([(255, 0, 0)] * duration_leds)  # Red for B4
#                     print(f"Detected B4 (71), Duration LEDs: {duration_leds}")  # Print when B4 is detected
#             elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
#                 if msg.note == 69:
#                     led_a4_array.extend([(0, 0, 0)] * duration_leds)  # Off for A4
#                 elif msg.note == 71:
#                     led_b4_array.extend([(0, 0, 0)] * duration_leds)  # Off for B4

#     return led_a4_array, led_b4_array

# # Main function -- right side of the LED strip for both notes
# def main():
#     # Create NeoPixel object with configuration
#     strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
#     strip.begin()

#     # Convert MIDI file to LED arrays
#     led_a4_array, led_b4_array = midi_to_led_arrays("output_two_notes.mid")

#     max_length = max(len(led_a4_array), len(led_b4_array))

#     # Debug: Print lengths of LED arrays
#     print(f"Length of A4 LED array: {len(led_a4_array)}")
#     print(f"Length of B4 LED array: {len(led_b4_array)}")

#     # Iterate through the maximum length of both LED arrays
#     for i in range(max_length + LED_COUNT):
#         # Shift all LEDs down by one position starting from LED 59 for A4
#         for j in range(LED_COUNT - 1, 30, -1):  # Start from the last LED
#             strip.setPixelColor(j, strip.getPixelColor(j - 1))
        
#         # Shift all LEDs up by one position starting from LED 29 for B4
#         for j in range(29, 0, -1):  # Start from LED 29 to 0
#             strip.setPixelColor(j, strip.getPixelColor(j - 1))
        
#         # Set the 30th LED (index 29) to the current color for B4
#         if i < len(led_b4_array):
#             color_b4 = Color(*led_b4_array[i])
#         else:
#             color_b4 = Color(0, 0, 0)  # Turn off the LED
        
#         strip.setPixelColor(0, color_b4)  # Set the first LED for B4
        
#         # Debug: Print current color for B4
#         print(f"Step {i}: B4 Color - {color_b4}, Position: 0")

#         # Set the 31st LED (index 30) to the current color for A4
#         if i < len(led_a4_array):
#             color_a4 = Color(*led_a4_array[i])
#         else:
#             color_a4 = Color(0, 0, 0)  # Turn off the LED
        
#         strip.setPixelColor(30, color_a4)  # Set the 31st LED for A4
        
#         # Debug: Print current color for A4
#         print(f"Step {i}: A4 Color - {color_a4}, Position: 30")

#         # Update the strip
#         strip.show()
        
#         # Delay to control the speed of the effect
#         time.sleep(0.1)  # Adjust the delay as needed

# if __name__ == "__main__":
#     main()