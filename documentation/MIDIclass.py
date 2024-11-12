# a program to parse and compare two MIDI files and produce statistics on their overlap
# Author: Olen Brown and Chaewon Shin
# import pretty_midi
'''
from collections import defaultdict

# MIDI file custom class
class MIDIfile:
    def __init__(self, midi_file_path, user_type):
        # create a dictionary of lists of tuples
        # the dictionary keys will be the names of the notes
        # the the lists will contain tuples of intervals
        # the tuples will be (start_time, end_time, user_type)
        self.data = defaultdict(list)
        self.file_path = midi_file_path
        self.user_type = user_type
        self.extract_notes(self.file_path)
        print("ran init")

    
    def extract_notes(midi_file):
        midi_data = pretty_midi.PrettyMIDI(midi_file)

        # Merge all notes from all instruments
        # do we need to check all instruments or will there always be just the one?
        all_notes = []
        for instrument in midi_data.instruments:
            all_notes.extend(instrument.notes)
            print(instrument.name)

        # Sort all notes by their start time
        # why do we need the notes sorted?
        sorted_notes = sorted(all_notes, key=lambda note: note.start)

        # Print details of the notes in order
        for idx, note in enumerate(sorted_notes):
            note_name = pretty_midi.note_number_to_name(note.pitch)
            print(f"Note {idx + 1}: {note_name}, " 
                f"Start: {note.start:.2f}s, End: {note.end:.2f}s")
        return sorted_notes


    def construct_interval_tree():
        return 0
'''
def main():
    # myFile = MIDIfile("Happy_Birthday_To_You_Piano.mid", "website")
    print("complete")

