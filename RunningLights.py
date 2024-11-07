# from rpi_ws281x import PixelStrip, Color
# import time
# from PIL import Image, ImageDraw, ImageFont

# # LED matrix configuration:
# LED_WIDTH = 50          # Number of LEDs in the width (columns)
# LED_HEIGHT = 40         # Number of LEDs in the height (rows)
# LED_COUNT = LED_WIDTH * LED_HEIGHT  # Total number of LEDs
# LED_PIN = 18            # GPIO pin connected to the pixels (must support PWM!)
# LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800kHz)
# LED_DMA = 10            # DMA channel to use for generating signal (try 10)
# LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
# LED_INVERT = False      # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL = 0         # Set to 1 for GPIOs 13, 19, 41, 45 or 53

# # Create a mapping from 2D coordinates to 1D LED strip index
# def get_led_index(x, y):
#     if y % 2 == 0:
#         # Even rows run left to right
#         index = y * LED_WIDTH + x
#     else:
#         # Odd rows run right to left
#         index = y * LED_WIDTH + (LED_WIDTH - 1 - x)
#     return index

# def main():
#     # Initialize the LED strip
#     strip = PixelStrip(
#         LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
#     )
#     strip.begin()

#     # Create an image with the text
#     text = "NotesArt!"
#     font_size = 16  # Adjust font size as needed
#     font = ImageFont.truetype(
#         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size
#     )

#     # Measure the size of the text
#     text_width, text_height = font.getsize(text)

#     # Create an image large enough to hold the text
#     image = Image.new("RGB", (text_width, text_height), "black")
#     draw = ImageDraw.Draw(image)
#     text_x = 0  # Left of the image
#     text_y = 0  # Top of the image
#     draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

#     # Rotate the image 90 degrees to the right
#     rotated_image = image.rotate(-90, expand=True)

#     # Calculate new dimensions after rotation
#     rotated_width, rotated_height = rotated_image.size

#     # Create a full image that is taller to allow scrolling from off-screen
#     full_image_width = LED_WIDTH
#     full_image_height = rotated_height + (2 * LED_HEIGHT)  # Add extra height for scrolling and off-screen start
#     full_image = Image.new("RGB", (full_image_width, full_image_height), "black")

#     # Paste the rotated text image onto the full image with an offset to start off-screen
#     text_x = (full_image_width - rotated_width) // 2  # Center horizontally
#     text_y = LED_HEIGHT  # Offset by LED_HEIGHT to start off-screen
#     full_image.paste(rotated_image, (text_x, text_y))

#     # Animation parameters
#     frame_delay = 0.05  # Time between frames in seconds
#     total_frames = full_image_height - LED_HEIGHT + 1  # Total number of frames for scrolling

#     # Animate the text moving from top to bottom
#     for offset_y in range(0, total_frames):
#         start_time = time.time()
#         # Create a frame by cropping the full image
#         frame = full_image.crop((0, offset_y, LED_WIDTH, offset_y + LED_HEIGHT))

#         # Update LEDs based on the frame
#         for y in range(LED_HEIGHT):
#             for x in range(LED_WIDTH):
#                 r, g, b = frame.getpixel((x, y))
#                 index = get_led_index(x, y)
#                 strip.setPixelColor(index, Color(r, g, b))
#         strip.show()

#         # Wait to maintain frame rate
#         elapsed = time.time() - start_time
#         sleep_time = frame_delay - elapsed
#         if sleep_time > 0:
#             time.sleep(sleep_time)

#     # Clear the strip after animation
#     for i in range(strip.numPixels()):
#         strip.setPixelColor(i, Color(0, 0, 0))
#     strip.show()

# if __name__ == "__main__":
#     main()






# # import numpy as np
# # from mido import MidiFile
# # import time
# # from rpi_ws281x import PixelStrip, Color

# # # Constants for LED strip
# # LED_COUNT      = 1800    # Total number of LEDs (36 notes * 50 LEDs per note)
# # LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!)
# # LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800kHz)
# # LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
# # LED_BRIGHTNESS = 150     # Set to 0 for darkest and 255 for brightest
# # LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
# # LED_CHANNEL    = 0       # Set to 1 for GPIOs 13, 19, 41, 45 or 53

# # # Function to convert a single MIDI file to LED arrays for specified notes
# # def midi_to_led_arrays(midi_file_path, notes, colors, alt_colors):
# #     midi = MidiFile(midi_file_path)
# #     led_arrays = {note: [] for note in notes}
# #     note_on_times = {note: [] for note in notes}
# #     last_note_end_times = {note: 0 for note in notes}
# #     consecutive_note_counts = {note: -1 for note in notes}  # Start at -1 for correct alternation

# #     led_per_tick = 4 / midi.ticks_per_beat  # Number of LEDs per tick (assuming 4 LEDs per beat)
# #     rest_threshold_ticks = midi.ticks_per_beat * 0.05  # Adjust the threshold as needed (e.g., 5% of a beat)

# #     for track in midi.tracks:
# #         current_time = 0
# #         for msg in track:
# #             current_time += msg.time
# #             if msg.type == 'note_on' and msg.velocity > 0 and msg.note in notes:
# #                 note_on_times[msg.note].append(current_time)
# #                 print(f"Note On: {msg}, Current Time: {current_time}")
# #             elif ((msg.type == 'note_off' and msg.note in notes) or
# #                   (msg.type == 'note_on' and msg.velocity == 0 and msg.note in notes)):
# #                 if note_on_times[msg.note]:
# #                     note_on_time = note_on_times[msg.note].pop(0)
# #                     duration_ticks = current_time - note_on_time
# #                     duration_leds = int(duration_ticks * led_per_tick)

# #                     # Determine if there was a significant rest before this note
# #                     gap_ticks = note_on_time - last_note_end_times[msg.note]
# #                     if gap_ticks > rest_threshold_ticks:
# #                         # There was a rest, reset consecutive note count
# #                         rest_leds = int(gap_ticks * led_per_tick)
# #                         led_arrays[msg.note].extend([(0, 0, 0)] * rest_leds)
# #                         consecutive_note_counts[msg.note] = -1  # Start at -1 to use base color first
# #                     else:
# #                         # No significant rest
# #                         # If there is a small gap, fill it without resetting the count
# #                         if gap_ticks > 0:
# #                             gap_leds = int(gap_ticks * led_per_tick)
# #                             led_arrays[msg.note].extend([(0, 0, 0)] * gap_leds)

# #                     # Increment the consecutive note count
# #                     consecutive_note_counts[msg.note] += 1

# #                     # Alternate color for consecutive notes
# #                     note_index = notes.index(msg.note)
# #                     base_color = colors[note_index]
# #                     alternate_color = alt_colors[note_index]
# #                     if consecutive_note_counts[msg.note] % 2 == 0:
# #                         # Use base color on even counts
# #                         used_color = base_color
# #                     else:
# #                         # Use alternate (darker) color on odd counts
# #                         used_color = alternate_color

# #                     led_arrays[msg.note].extend([used_color] * duration_leds)
# #                     last_note_end_times[msg.note] = current_time
# #                     print(f"Note Off: {msg}, Duration Ticks: {duration_ticks}, Duration LEDs: {duration_leds}")
# #                 else:
# #                     print(f"Note Off without Note On: {msg}, Current Time: {current_time}")

# #     return led_arrays

# # # Main function
# # def main():
# #     # Create NeoPixel object with configuration
# #     strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# #     strip.begin()

# #     # Define notes for C2 to B4 (36 notes)
# #     notes = list(range(36, 72))  # MIDI notes from C2 (36) to B4 (71)

# #     # Identify white and black keys for each octave
# #     # Octave 2 (C2 to B2)
# #     white_keys_octave2 = [36, 38, 40, 41, 43, 45, 47]
# #     black_keys_octave2 = [37, 39, 42, 44, 46]

# #     # Octave 3 (C3 to B3)
# #     white_keys_octave3 = [48, 50, 52, 53, 55, 57, 59]
# #     black_keys_octave3 = [49, 51, 54, 56, 58]

# #     # Octave 4 (C4 to B4)
# #     white_keys_octave4 = [60, 62, 64, 65, 67, 69, 71]
# #     black_keys_octave4 = [61, 63, 66, 68, 70]

# #     colors = []
# #     alt_colors = []

# #     for note in notes:
# #         if note in white_keys_octave2:
# #             colors.append((255, 0, 0))      # Base red for octave 2 white keys
# #             alt_colors.append((255, 255, 255))  # White for alternation
# #         elif note in black_keys_octave2:
# #             colors.append((153, 0, 153))    # Base purple for octave 2 black keys
# #             alt_colors.append((255, 255, 255))  # White for alternation
# #         elif note in white_keys_octave3:
# #             colors.append((0, 255, 0))      # Base green for octave 3 white keys
# #             alt_colors.append((255, 255, 255))  # White for alternation
# #         elif note in black_keys_octave3:
# #             colors.append((153, 0, 153))    # Base purple for octave 2 black keys
# #             alt_colors.append((255, 255, 255))  # White for alternation
# #         elif note in white_keys_octave4:
# #             colors.append((0, 0, 255))    # Base blue for octave 4 white keys
# #             alt_colors.append((255, 255, 255))  # White for alternation
# #         elif note in black_keys_octave4:
# #             colors.append((153, 0, 153))    # Base purple for octave 2 black keys
# #             alt_colors.append((255, 255, 255))  # White for alternation
# #         else:
# #             colors.append((0, 0, 0))        # Default to black if note is not identified
# #             alt_colors.append((0, 0, 0))

# #     # Print colors for debugging
# #     print("Colors:", colors)
# #     print("Alt Colors:", alt_colors)

# #     # Convert MIDI file to LED arrays for the notes
# #     midi_file_path = "../midi_files/mary_right_hand.mid"  # Replace with your MIDI file path
# #     led_arrays = midi_to_led_arrays(midi_file_path, notes, colors, alt_colors)

# #     # Print the LED arrays for debugging
# #     for note in notes:
# #         print(f"LED Array Length for Note {note}:", len(led_arrays[note]))
# #         # Uncomment the next line if you want to print the entire array (can be long)
# #         # print(f"LED Array for Note {note}:", led_arrays[note])

# #     # Each note gets 50 LEDs
# #     leds_per_note = 50
# #     total_leds_needed = leds_per_note * len(notes)
# #     if total_leds_needed > LED_COUNT:
# #         print(f"Error: Not enough LEDs. Required: {total_leds_needed}, Available: {LED_COUNT}")
# #         return

# #     # Prepare led_strips
# #     led_strips = {}
# #     for idx, note in enumerate(notes):
# #         led_strips[note] = [(0, 0, 0)] * leds_per_note

# #     # Find the maximum length among all led_arrays
# #     max_length = max(len(led_arrays[note]) for note in notes) + leds_per_note

# #     frame_duration = 0.2  # Desired frame duration in seconds

# #     for i in range(max_length):
# #         start_time = time.time()
# #         for idx, note in enumerate(notes):
# #             start_index = idx * leds_per_note
# #             end_index = start_index + leds_per_note
# #             section_length = leds_per_note
# #             led_strip = led_strips[note]
# #             led_array = led_arrays[note]

# #             # Shift and update led_strip for each note
# #             if idx % 2 == 0:
# #                 # Left shift
# #                 for j in range(section_length - 1):
# #                     led_strip[j] = led_strip[j + 1]
# #                 if i < len(led_array):
# #                     led_strip[section_length - 1] = led_array[i]
# #                 else:
# #                     led_strip[section_length - 1] = (0, 0, 0)
# #             else:
# #                 # Right shift
# #                 for j in range(section_length - 1, 0, -1):
# #                     led_strip[j] = led_strip[j - 1]
# #                 if i < len(led_array):
# #                     led_strip[0] = led_array[i]
# #                 else:
# #                     led_strip[0] = (0, 0, 0)
# #             led_strips[note] = led_strip

# #             # Update the strip for this section
# #             for k in range(section_length):
# #                 strip.setPixelColor(start_index + k, Color(*led_strip[k]))

# #         # After updating all sections, show the strip
# #         strip.show()

# #         # Calculate elapsed time and sleep to maintain frame rate
# #         elapsed_time = time.time() - start_time
# #         time_to_sleep = frame_duration - elapsed_time
# #         if time_to_sleep > 0:
# #             time.sleep(time_to_sleep)

# #     # Clear the strip at the end
# #     clear_strip(strip)

# # def clear_strip(strip):
# #     for i in range(LED_COUNT):
# #         strip.setPixelColor(i, Color(0, 0, 0))
# #     strip.show()

# # if __name__ == "__main__":
# #     main()

from rpi_ws281x import PixelStrip, Color
import time
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from mido import MidiFile

# LED matrix configuration:
LED_WIDTH = 50          # Number of LEDs in the width (columns)
LED_HEIGHT = 40         # Number of LEDs in the height (rows)
LED_COUNT = LED_WIDTH * LED_HEIGHT  # Total number of LEDs (2000)
LED_PIN = 18            # GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ = 800000    # LED signal frequency in hertz (usually 800kHz)
LED_DMA = 10            # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT = False      # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0         # Set to 1 for GPIOs 13, 19, 41, 45 or 53

# Create a mapping from 2D coordinates to 1D LED strip index
def get_led_index(x, y):
    if y % 2 == 0:
        # Even rows run left to right
        index = y * LED_WIDTH + x
    else:
        # Odd rows run right to left
        index = y * LED_WIDTH + (LED_WIDTH - 1 - x)
    return index

# Function to clear the strip
def clear_strip(strip):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

# Function to run the MIDI visualization
def run_midi_visualization(strip, song_file):
    # Define notes for C2 to B4 (36 notes)
    notes = list(range(36, 72))  # MIDI notes from C2 (36) to B4 (71)

    # Identify white and black keys for each octave
    # Octave 2 (C2 to B2)
    white_keys_octave2 = [36, 38, 40, 41, 43, 45, 47]
    black_keys_octave2 = [37, 39, 42, 44, 46]

    # Octave 3 (C3 to B3)
    white_keys_octave3 = [48, 50, 52, 53, 55, 57, 59]
    black_keys_octave3 = [49, 51, 54, 56, 58]

    # Octave 4 (C4 to B4)
    white_keys_octave4 = [60, 62, 64, 65, 67, 69, 71]
    black_keys_octave4 = [61, 63, 66, 68, 70]

    colors = []
    alt_colors = []

    for note in notes:
        if note in white_keys_octave2:
            colors.append((255, 0, 0))      # Base red for octave 2 white keys
            alt_colors.append((255, 255, 255))  # White for alternation
        elif note in black_keys_octave2:
            colors.append((153, 0, 153))    # Base purple for octave 2 black keys
            alt_colors.append((255, 255, 255))  # White for alternation
        elif note in white_keys_octave3:
            colors.append((0, 255, 0))      # Base green for octave 3 white keys
            alt_colors.append((255, 255, 255))  # White for alternation
        elif note in black_keys_octave3:
            colors.append((153, 0, 153))    # Base purple for octave 3 black keys
            alt_colors.append((255, 255, 255))  # White for alternation
        elif note in white_keys_octave4:
            colors.append((0, 0, 255))    # Base blue for octave 4 white keys
            alt_colors.append((255, 255, 255))  # White for alternation
        elif note in black_keys_octave4:
            colors.append((153, 0, 153))    # Base purple for octave 4 black keys
            alt_colors.append((255, 255, 255))  # White for alternation
        else:
            colors.append((0, 0, 0))        # Default to black if note is not identified
            alt_colors.append((0, 0, 0))

    # Convert MIDI file to LED arrays for the notes
    midi_file_path = "songs/{song_file}"  # Replace with your MIDI file path
    led_arrays = midi_to_led_arrays(midi_file_path, notes, colors, alt_colors)

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

    frame_duration = 0.2  # Desired frame duration in seconds

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
                color = led_strip[k]
                r, g, b = color
                strip.setPixelColor(start_index + k, Color(r, g, b))

        # After updating all sections, show the strip
        strip.show()

        # Calculate elapsed time and sleep to maintain frame rate
        elapsed_time = time.time() - start_time
        time_to_sleep = frame_duration - elapsed_time
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    # Clear the strip at the end
    clear_strip(strip)

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
                        # Use alternate color on odd counts
                        used_color = alternate_color

                    led_arrays[msg.note].extend([used_color] * duration_leds)
                    last_note_end_times[msg.note] = current_time
                else:
                    pass  # Note off without corresponding note on

    return led_arrays

# Function to run the "NotesArt!" animation
def run_notesart_animation(strip):
    # Create an image with the text
    text = "NotesArt!"
    font_size = 16  # Adjust font size as needed
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size
    )

    # Measure the size of the text
    text_width, text_height = font.getsize(text)

    # Create an image large enough to hold the text
    image = Image.new("RGB", (text_width, text_height), "black")
    draw = ImageDraw.Draw(image)
    text_x = 0  # Left of the image
    text_y = 0  # Top of the image
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255))

    # Rotate the image 90 degrees to the right
    rotated_image = image.rotate(-90, expand=True)

    # Calculate new dimensions after rotation
    rotated_width, rotated_height = rotated_image.size

    # Create a full image that is taller to allow scrolling from off-screen
    full_image_width = LED_WIDTH
    full_image_height = rotated_height + (2 * LED_HEIGHT)  # Add extra height for scrolling and off-screen start
    full_image = Image.new("RGB", (full_image_width, full_image_height), "black")

    # Paste the rotated text image onto the full image with an offset to start off-screen
    text_x = (full_image_width - rotated_width) // 2  # Center horizontally
    text_y = LED_HEIGHT  # Offset by LED_HEIGHT to start off-screen
    full_image.paste(rotated_image, (text_x, text_y))

    # Animation parameters
    frame_delay = 0.05  # Time between frames in seconds
    total_frames = full_image_height - LED_HEIGHT + 1  # Total number of frames for scrolling

    # Animate the text moving from top to bottom
    for offset_y in range(0, total_frames):
        start_time = time.time()
        # Create a frame by cropping the full image
        frame = full_image.crop((0, offset_y, LED_WIDTH, offset_y + LED_HEIGHT))

        # Update LEDs based on the frame
        for y in range(LED_HEIGHT):
            for x in range(LED_WIDTH):
                r, g, b = frame.getpixel((x, y))
                index = get_led_index(x, y)
                strip.setPixelColor(index, Color(r, g, b))
        strip.show()

        # Wait to maintain frame rate
        elapsed = time.time() - start_time
        sleep_time = frame_delay - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    # Clear the strip after animation
    clear_strip(strip)

def main():
    import sys

    if len(sys.argv) > 1:
        song_file = sys.argv[1]
        print(f"Running with song file: {song_file}")
        # Add code to play or process the song file
    else:
        print("No song file provided.")

        # Initialize the LED strip
    strip = PixelStrip(
        LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
    )
    strip.begin()

    # Run the MIDI visualization first
    run_midi_visualization(strip, song_file)
    time.sleep(3)
    # After the MIDI visualization completes and the last note falls completely, run the "NotesArt!" animation
    run_notesart_animation(strip)

if __name__ == "__main__":
    main()
