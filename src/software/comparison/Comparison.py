# a program to parse and compare two MIDI files and produce statistics on their overlap
# Author: Olen Brown and Chaewon Shin

import pretty_midi
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 
import tkinter as tk
from tkinter import messagebox
import mido

# MIDI file custom class
class MIDIfile:
        # create a dictionary of lists of tuples
        # the dictionary keys will be the names of the notes
        # the the lists will contain tuples of intervals
        # the tuples will be (start_time, end_time, user_type)

    def __init__(self, midi_file_path):
        # Initialize the MIDIfile by loading the MIDI data and extracting notes
        self.midi_data = pretty_midi.PrettyMIDI(midi_file_path)
        self.extracted_notes = self.extract_notes()
        
        self.total_intervals = 0  # Track total number of notes
        
        self.note_intervals = {}
        self.get_note_intervals()
        
        def get_bpm(path):
            mid = mido.MidiFile(path)
            for track in mid.tracks:
                for msg in track:
                    if msg.type == 'set_tempo':
                        tempo = msg.tempo
                        bpm = mido.tempo2bpm(tempo)
                        return bpm
            return None 

        self.offset = None
        self.bpm = get_bpm(midi_file_path)
        self.offset = ((1/(self.bpm/60))/4 )*50  # Calculate the offset in seconds

        print("************************************")
        print(midi_file_path)
        print("offset: ", self.offset)
        for pitch in self.note_intervals:
           print(pitch, self.note_intervals[pitch])
        print("************************************")


    def extract_notes(self):
        # Extract all notes from all instruments in the MIDI file
        all_notes = []
        for instrument in self.midi_data.instruments:
            all_notes.extend(instrument.notes)
        # Sort all notes by their start time
        # sorted_notes = sorted(all_notes, key=lambda note: note.start)
        #print(" *sorted_notes* \n", sorted_notes)
        return all_notes

    def get_note_intervals(self):
        # Return a list of tuples containing (pitch, start time, end time, note name) for each note
        # pitch, start-time, end-time, note name 
        # return [(note.pitch, note.start, note.end, pretty_midi.note_number_to_name(note.pitch)) for note in self.notes]

        for note in self.extracted_notes:
            note_name = pretty_midi.note_number_to_name(note.pitch)

            if note_name not in self.note_intervals:
                self.note_intervals[note_name] = []

            self.note_intervals[note_name].append((note.start, note.end))
            self.total_intervals += 1  # Count each interval
              

def generate_by_note_stat(midi_ref_path, midi_user_path):
    midi_ref = MIDIfile(midi_ref_path) # unpack the reference midi file
    midi_user = MIDIfile(midi_user_path) # unpack the user midi file
 

    intervals_ref = midi_ref.note_intervals # reference midi intervals
    intervals_user = midi_user.note_intervals # user midi intervals

    offset = midi_ref.offset

    # dictionaires of correct notes and missed notes by pitch
    correct_notes = {}
    missed_notes = {}
    accuracy_notes = {}

    # populate the dictionaries with the pitches of the reference song as keys
    for pitch in intervals_ref:
        correct_notes[pitch] = []
        missed_notes[pitch] = []
        #accuracy_notes = -1
        if pitch not in intervals_user:
            intervals_user[pitch] = []

    tolerance = 1  # Tolerance in seconds for timing deviation

    for pitch in intervals_ref: # for every pitch in the reference song
        ref = intervals_ref[pitch] # gets the list of intervals from the reference
        user = intervals_user[pitch] # gets the list of intervals from the user
        for ref_start, ref_end in ref: # check the overlap of notes in ref with notes in user
            found = False
            for user_start, user_end in user:
                user_start -= offset
                user_end -= offset
                if abs(ref_start - user_start) <= tolerance and abs(ref_end - user_end) <= tolerance:
                    correct_notes[pitch].append(ref)
                    found = True
                    break
            if not found:
                missed_notes[pitch].append(ref)

    for pitch in intervals_ref:
        correct_total = len(correct_notes[pitch])
        missed_total = len(missed_notes[pitch])
        if correct_total + missed_total == 0:
            accuracy_notes[pitch] = 100
        else:
            accuracy_notes[pitch] = (correct_total / (correct_total + missed_total)) * 100
    
    return accuracy_notes
    
    
def total_accuracy(midi_ref_path, midi_user_path):
    # Load the MIDI files using the MIDIfile class
    midi_ref = MIDIfile(midi_ref_path)  # Reference MIDI file
    midi_user = MIDIfile(midi_user_path) # User-played MIDI file

    # Get note intervals (pitch, start time, end time) from both MIDI files
    intervals_ref = midi_ref.note_intervals  # Reference MIDI intervals 
    intervals_user = midi_user.note_intervals # User-played MIDI intervals 

    offset = midi_ref.offset


    # Initialize counters and dictionaries
    correct_notes = 0
    missed_notes = 0
    total_ref_notes = 0
    tolerance = 1  # Tolerance in seconds for timing deviation10

    # Iterate over each note (pitch) in the reference MIDI intervals
    for pitch in intervals_ref:
        ref_intervals = intervals_ref[pitch]  # Reference intervals for this pitch
        user_intervals = intervals_user.get(pitch, [])  # Get user intervals, default to empty if not found
        total_ref_notes += len(ref_intervals)  # Total notes in the reference for accuracy calculation

        for ref_start, ref_end in ref_intervals:
            found = False
            for user_start, user_end in user_intervals:
                user_start -= offset
                user_end -= offset
                if (abs(ref_start - user_start) <= tolerance and abs(ref_end - user_end) <= tolerance):
                    correct_notes += 1
                    found = True
                    break
            if not found:
                missed_notes += 1

    # Calculate the total accuracy
    if total_ref_notes > 0:
        total_accuracy = (correct_notes / total_ref_notes) * 100
    else:
        total_accuracy = 0

    # Print the performance results
    """
    print(f"Total reference intervals: {total_ref_notes}")
    print(f"Correct intervals: {correct_notes}")
    print(f"Missed intervals: {missed_notes}")
    print(f"Total accuracy: {total_accuracy:.2f}%")
    print("\n")
    """
    
    return f"{total_accuracy:.2f}"


def print_MIDI_details(midi_ref_path, midi_user_path):
    midi_ref = MIDIfile(midi_ref_path)  # Load reference MIDI
    midi_user = MIDIfile(midi_user_path)  # Load user MIDI

    # Get the list of pitch types from the reference and user files
    reference_pitches = list(midi_ref.note_intervals.keys())
    user_pitches = list(midi_user.note_intervals.keys())

    # Print the number of unique pitches and their types for the reference file
    print("[Reference file note details]")
    print(f"**Total unique pitches in reference file: {len(reference_pitches)}")
    print(f"**Pitches in reference file: {reference_pitches}")
    for pitch, intervals in midi_ref.note_intervals.items():
        print(f"Pitch: {pitch}, Intervals: {intervals}")
    print(f"**Total intervals in reference file: {midi_ref.total_intervals}")

    # Print the number of unique pitches and their types for the user file
    print("\n[User file note details]")
    print(f"**Total unique pitches in user file: {len(user_pitches)}")
    print(f"**Pitches in user file: {user_pitches}")
    for pitch, intervals in midi_user.note_intervals.items():
        print(f"Pitch: {pitch}, Intervals: {intervals}")
    print(f"**Total intervals in user file: {midi_user.total_intervals}")
    print("\n")


# Display accuracy stats in a pop-up window
def display_results(midi_ref, midi_user, total_acc, accuracy_by_notes):
    root = tk.Tk()
    root.withdraw()

    # Create a message with the accuracy stats
    message = f"Reference MIDI file: {midi_ref}\n"
    message += f"User MIDI file: {midi_user}\n\n"

    message += f"Total Accuracy: {total_acc:.2f}%\n\n"

    message += "Accuracy by Note (Pitch):\n"
    for pitch, accuracy in accuracy_by_notes.items():
        message += f"Pitch: {pitch}, Accuracy: {accuracy:.2f}%\n"
    messagebox.showinfo("MIDI Accuracy Results", message)


# Happy_Birthday_Easy_to_play.mid
# Happy_Birthday_To_You_Piano.mid
#compare_midi_files("Happy_Birthday_Easy_to_play.mid", "Happy_Birthday_To_You_Piano.mid") # user-played song, reference song
# by_note_output
'''
# Name of MIDI files
midi_reference = "Happy_Birthday_Easy_to_play.mid"
#midi_reference = "user.mid"
midi_user = "user.mid"

# Print MIDI file Details (pitch, intervals)
#print_MIDI_details(midi_reference, midi_user)

# Compare two different MIDI songs
# Accuracy Stats
total_acc = total_accuracy(midi_reference, midi_user)
accuracy_by_notes = generate_by_note_stat(midi_reference, midi_user)
# Print the accuracy for each note (pitch)
"""
print("Accuracy by Note (Pitch):")
for pitch, accuracy in accuracy_by_notes.items():
    print(f"Pitch: {pitch}, Accuracy: {accuracy:.2f}%")
"""
# Display the results in a pop-up window
# display_results(midi_reference, midi_user, total_acc, accuracy_by_notes)
'''