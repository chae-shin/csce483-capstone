import sys
import os
from mido import MidiFile, MidiTrack, Message, MetaMessage

def get_note_name(pitch):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (pitch // 12) - 1
    note = note_names[pitch % 12]
    return f'{note}{octave}'

def process_midi(input_file, output_dir):
    mid = MidiFile(input_file)

    # Collect all unique pitches
    unique_pitches = set()
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                unique_pitches.add(msg.note)

    for pitch in unique_pitches:
        output_mid = MidiFile()
        # Copy the attributes of the original file
        output_mid.ticks_per_beat = mid.ticks_per_beat
        # For each track in the original file, create a corresponding track
        for i, track in enumerate(mid.tracks):
            output_track = MidiTrack()
            output_mid.tracks.append(output_track)
            # Initialize cumulative time
            cumulative_time = 0
            # List to store included messages
            included_messages = []
            for msg in track:
                cumulative_time += msg.time
                if isinstance(msg, MetaMessage):
                    # Include all meta messages
                    included_messages.append((cumulative_time, msg))
                elif msg.type == 'note_on' or msg.type == 'note_off':
                    if msg.note == pitch:
                        # Include the message
                        included_messages.append((cumulative_time, msg))
                else:
                    # Include other messages
                    included_messages.append((cumulative_time, msg))
            # Now compute delta times between included messages
            last_time = 0
            for time, msg in included_messages:
                delta_time = time - last_time
                last_time = time
                new_msg = msg.copy(time=delta_time)
                output_track.append(new_msg)
        # Save the output file
        note_name = get_note_name(pitch)
        output_filename = f'note_{note_name}.mid'
        output_path = os.path.join(output_dir, output_filename)
        output_mid.save(output_path)
        print(f"Saved {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python separate_notes.py input.mid [output_directory]")
    else:
        input_file = sys.argv[1]
        if len(sys.argv) == 3:
            output_dir = sys.argv[2]
        else:
            output_dir = '.'
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        process_midi(input_file, output_dir)
