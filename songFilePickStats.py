import pretty_midi
import os


def song_data():
    song_data = []
    folder_path = 'songs/'
    for filename in os.listdir(folder_path):
        if filename.endswith('.mid'):
            midi_file_path = os.path.join(folder_path, filename)
            midi_data = pretty_midi.PrettyMIDI(midi_file_path)

            duration = midi_data.get_end_time()

            song_data.append({
                'name': filename,
                'duration': f"{duration:.2f} seconds",
                'difficulty': 'easy'
            })

            # print(f"Duration of {filename}: {duration:.2f} seconds")
    return song_data