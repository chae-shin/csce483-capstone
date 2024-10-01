import mido
from mido import MidiFile, MidiTrack, Message

# Define your output .py file
output_file = "write.txt"

# Open MIDI input
input_name = mido.get_input_names()[0]  # Select the first MIDI input device
with mido.open_input(input_name) as port:
    notes = []
    print("Playing... (Press Ctrl+C to stop)")
    