import pretty_midi
import os

def song_data():
    song_data_list = []
    folder_path = 'songs/'
    for filename in os.listdir(folder_path):
        if filename.endswith('.mid'):
            midi_file_path = os.path.join(folder_path, filename)
            midi_data = pretty_midi.PrettyMIDI(midi_file_path)
            duration = midi_data.get_end_time()
            difficulty_bpm = midi_data.estimate_tempo()
            
            if difficulty_bpm <= 100.0:
                difficulty = 'Easy'
            elif difficulty_bpm <=150.0:
                difficulty = 'Medium'
            else:
                difficulty = 'Hard'

            song_data_list.append({
                'name': filename,
                'duration': f"{duration:.2f} seconds",
                'difficulty': difficulty
            })
    return song_data_list
