# import mido # MIDI library

# mid = mido.MidiFile('Happy_Birthday_To_You_Piano.mid')
# for msg in mid.play():
#     print(msg)

# -------------
# this code just prints all the notes in the midi file in order, so like prints the notes in subsequent order
# import pretty_midi

# # Load your MIDI file
# midi_data = pretty_midi.PrettyMIDI('Happy_Birthday_To_You_Piano.mid')

# # Print the basic information about the MIDI file
# print(f"Number of tracks: {len(midi_data.instruments)}")
# print(f"Tempo: {midi_data.estimate_tempo()} BPM")

# # Iterate through each instrument in the file
# for i, instrument in enumerate(midi_data.instruments):
#     print(f"\nInstrument {i + 1}:")
#     print(f"Instrument Name: {pretty_midi.program_to_instrument_name(instrument.program)}")
#     print(f"Is Drum: {instrument.is_drum}")
#     print(f"Number of Notes: {len(instrument.notes)}")

#     sorted_notes = sorted(instrument.notes, key=lambda note: note.start)


#     # Print details of the notes in order
#     for idx, note in enumerate(sorted_notes):
#         note_name = pretty_midi.note_number_to_name(note.pitch)
#         print(f"Note {idx + 1}: {note_name}, Pitch: {note.pitch}, "
#               f"Start: {note.start:.2f}s, End: {note.end:.2f}s, Velocity: {note.velocity}")

# -------------
# this code will print all the notes together from the 2 instruments, and print them of order of their start time
import pretty_midi

# Load your MIDI file
midi_data = pretty_midi.PrettyMIDI('Happy_Birthday_To_You_Piano.mid')

# Merge all notes from all instruments
all_notes = []
for instrument in midi_data.instruments:
    all_notes.extend(instrument.notes)

# Sort all notes by their start time
sorted_notes = sorted(all_notes, key=lambda note: note.start)

# Print details of the notes in order
for idx, note in enumerate(sorted_notes):
    note_name = pretty_midi.note_number_to_name(note.pitch)
    print(f"Note {idx + 1}: {note_name}, Pitch: {note.pitch}, "
          f"Start: {note.start:.2f}s, End: {note.end:.2f}s, Velocity: {note.velocity}")