# a program to parse and compare two MIDI files and produce statistics on their overlap
# Author: Olen Brown and Chaewon Shin
import pretty_midi

# MIDI file custom class
class MIDIfile:
    def __init__(self, midi_file_path, user_type):
        # create a dictionary of lists of tuples
        # the dictionary keys will be the names of the notes
        # the the lists will contain tuples of intervals
        # the tuples will be (start_time, end_time, user_type)
        
        
        
    

def extract_notes(midi_file):
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    # Merge all notes from all instruments
    all_notes = []
    for instrument in midi_data.instruments:
        all_notes.extend(instrument.notes)

    # Sort all notes by their start time
    sorted_notes = sorted(all_notes, key=lambda note: note.start)

    # Print details of the notes in order
    for idx, note in enumerate(sorted_notes):
        note_name = pretty_midi.note_number_to_name(note.pitch)
        print(f"Note {idx + 1}: {note_name}, " 
              f"Start: {note.start:.2f}s, End: {note.end:.2f}s")
    return sorted_notes


def compare_midi_files(midi_1, midi_2):
    
    note_1 = extract_notes(midi_1)
    note_2 = extract_notes(midi_2)
    

def construct_interval_tree():

