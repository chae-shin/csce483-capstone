import i2c_def as I2C_LCD_driver
from time import sleep
import pygame

display = I2C_LCD_driver.lcd()

def play_midi(file_path):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MIDI file
    pygame.mixer.music.load(file_path)

    # Get the length of the MIDI file
    midi_length = pygame.mixer.Sound(file_path).get_length()

    # Play the MIDI file
    pygame.mixer.music.play()

    # Wait for music to finish and update the progress on the LCD
    elapsed_time = 0
    bar_length = 16  # Length of the progress bar on the LCD
    while pygame.mixer.music.get_busy():
        sleep(1)
        elapsed_time += 1
        progress = min((elapsed_time / midi_length) * 100, 100)  # Ensure progress does not exceed 100%
        bar_filled_length = int(bar_length * (elapsed_time / midi_length))
        bar = '.' * bar_filled_length + ' ' * (bar_length - bar_filled_length)
        display.lcd_display_string(f"{file_path.split('/')[-1][:10]} {progress:.0f}%", 1)
        display.lcd_display_string(bar, 2)

    # Ensure the display shows 100% when finished
    display.lcd_display_string(f"{file_path.split('/')[-1][:10]} 100%", 1)
    display.lcd_display_string('.' * bar_length, 2)

# MIDI File path
midi_file = "../led/output_dummy_note.mid"

# Display the MIDI file name on the LCD
display.lcd_display_string(midi_file.split('/')[-1][:10], 1)

# Play the MIDI file
play_midi(midi_file)