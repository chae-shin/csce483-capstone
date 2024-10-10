# a program to parse and compare two MIDI files and produce statistics on their overlap
# Author: Olen Brown and Chaewon Shin

import pretty_midi

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

        self.note_intervals = {}
        self.get_note_intervals()

    def extract_notes(self):
        # Extract all notes from all instruments in the MIDI file
        all_notes = []
        for instrument in self.midi_data.instruments:
            all_notes.extend(instrument.notes)
        # Sort all notes by their start time
        # sorted_notes = sorted(all_notes, key=lambda note: note.start)
        # print(" *sorted_notes* \n", sorted_notes)
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


def compare_midi_files(midi_1_path, midi_2_path):

    # Load the MIDI files using the MIDIfile class
    midi_1 = MIDIfile(midi_1_path) # user played MIDI file
    midi_2 = MIDIfile(midi_2_path) # reference MIDI file

    # Get note intervals (pitch, start time, end time) from both MIDI files
    intervals_1 = midi_1.get_note_intervals() # user played MIDI file
    intervals_2 = midi_2.get_note_intervals() # reference MIDI file

    correct_notes = 0
    correct_notes_list = []
    missed_notes = 0
    missed_notes_list = []
    tolerance = 0.2  # Tolerance in seconds for timing deviation

    # Compare each note in the reference MIDI file to the user-played MIDI file
    for pitch_2, start_2, end_2, note_name_2 in intervals_2:
        matched = False
        for pitch_1, start_1, end_1, note_name_1 in intervals_1:
            # Check if the pitch matches, note name matches, and if both start and end times are within the tolerance
            if (pitch_1 == pitch_2 and note_name_1 == note_name_2 and
                    abs(start_1 - start_2) <= tolerance and abs(end_1 - end_2) <= tolerance):
                correct_notes_list.append((pitch_1, start_1, end_1, note_name_1))
                correct_notes += 1
                matched = True
                break
        if not matched:
            # If no match is found, add the note to the list of missed notes
            missed_notes += 1
            missed_notes_list.append((pitch_2, start_2, end_2, note_name_2))

    # Calculate the accuracy as a percentage
    total_notes = len(intervals_2)  # Total number of notes in the reference MIDI file
    if total_notes > 0:
        accuracy = (correct_notes / total_notes) * 100
    else:
        accuracy = 0

    # Print the performance results
    print(f"Total notes: {total_notes}")
    print(f"Accuracy: {accuracy:.2f}%")
    
    print(f"Correct notes: {correct_notes}")
    if not correct_notes_list:
        print("No Correct Notes!")
    else:
        # Print: the details of the correct notes
        for pitch, start, end, note_name in correct_notes_list:
            print(f"Pitch: {pitch}, Note: {note_name}, Start: {start:.2f}s, End: {end:.2f}s")

    print(f"Missed notes: {missed_notes}")
    if not missed_notes_list:
        print("No Missed Notes!")
    else:
        # Print the details of the missed notes
        for pitch, start, end, note_name in missed_notes_list:
            print(f"Pitch: {pitch}, Note: {note_name}, Start: {start:.2f}s, End: {end:.2f}s")

# Compare two different MIDI songs
# Happy_Birthday_Easy_to_play.mid
# Happy_Birthday_To_You_Piano.mid
#compare_midi_files("Happy_Birthday_Easy_to_play.mid", "Happy_Birthday_To_You_Piano.mid") # user-played song, reference song

midi = MIDIfile("Happy_Birthday_Easy_to_play.mid")
