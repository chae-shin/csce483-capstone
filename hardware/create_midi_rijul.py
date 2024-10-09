from midiutil import MIDIFile

# Create a MIDIFile object with one track
midi = MIDIFile(1)

# Track, Time, Tempo
track = 0
time = 0
tempo = 120
midi.addTempo(track, time, tempo)

# Track, Time, Numerator, Denominator, Clocks_per_click, 32nd_notes_per_24_midi_clocks
midi.addTimeSignature(track, time, 4, 2, 24, 8)

# Note parameters
channel = 0
pitch = 69  # MIDI note number for A4
volume = 100

# Add a dummy test note at the start
dummy_duration = 0.1  # Short duration for the dummy note
dummy_volume = 10     # Low volume for the dummy note
midi.addNote(track, channel, pitch, time, dummy_duration, dummy_volume)
time += dummy_duration  # Move time forward by the duration of the dummy note

# Add notes and rests with varying durations
durations = [4, 2, 1, 0.5]  # Whole note, half note, quarter note, eighth note

for duration in durations:
    midi.addNote(track, channel, pitch, time, duration, volume)
    time += duration  # Move time forward by the duration of the note
    time += duration  # Move time forward by the duration of the rest

# Add a dummy test note at the end
midi.addNote(track, channel, pitch, time, dummy_duration, dummy_volume)

# Write the MIDI data to a file
with open("output_dummy_note.mid", "wb") as output_file:
    midi.writeFile(output_file)