# import mido # MIDI library

# mid = mido.MidiFile('Happy_Birthday_To_You_Piano.mid')
# for msg in mid.play():
#     print(msg)

# -------------
import pretty_midi

# Load your MIDI file
midi_data = pretty_midi.PrettyMIDI('Happy_Birthday_Easy_to_play.mid')

# Print the basic information about the MIDI file
print(f"Number of tracks: {len(midi_data.instruments)}")
print(f"Tempo: {midi_data.estimate_tempo()} BPM")

# Iterate through each instrument in the file
for i, instrument in enumerate(midi_data.instruments):
    print(f"\nInstrument {i + 1}:")
    print(f"Instrument Name: {pretty_midi.program_to_instrument_name(instrument.program)}")
    print(f"Is Drum: {instrument.is_drum}")
    print(f"Number of Notes: {len(instrument.notes)}")

    # Print details of the first 10 notes
    for note in instrument.notes:
        note_name = pretty_midi.note_number_to_name(note.pitch)
        print(f"Note: {note_name}, Pitch: {note.pitch}, "
              f"Start: {note.start:.2f}s, End: {note.end:.2f}s, Velocity: {note.velocity}")

# -------------


# Print all General MIDI instrument names
# for program in range(128):
#     print(f"Program {program}: {pretty_midi.program_to_instrument_name(program)}")