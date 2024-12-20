from flask import Flask, render_template, request, jsonify
from songFilePickStats import song_data
import subprocess
import sys
import os
import subprocess
import signal
import pretty_midi
import mido

# sys.path.append(os.path.abspath("../user_input"))
# import src.software.user_input.piano_to_midi as piano_to_midi


sys.path.append(os.path.abspath("/home/capstone/csce483-capstone/src/software/comparison"))
# print(sys.path)

from Comparison import total_accuracy, generate_by_note_stat



app = Flask(__name__)

UPLOAD_FOLDER = '/home/capstone/csce483-capstone/songs/'
#UPLOAD_FOLDER = 'songs/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define song_file (song name)
song_file = None

@app.route("/")
def home():
    data = song_data()
    return render_template("index.html", song_data=data)

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'filename' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    file = request.files['filename']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({"status": "success", "message": "File uploaded successfully!"})

@app.route('/get_songs', methods=['GET'])
def get_songs():
    data = song_data()
    return jsonify(data)

@app.route("/play_song", methods=["POST"])
def play_song():
    global song_file
    data = request.get_json()
    song_index = data.get("song_name")
    # song_duration = data.get()

    try:
        # Run the specific Python file based on the song index
        song_file = song_index  # Adjust file path as needed
        print(song_file)
        # subprocess.run(["python3", "RunningLights.py", song_file], check=True)
        # subprocess.run(["python3", "diddy.py", song_file], check=True)
        
        # Popen should run the processes in parallel
        processLights = subprocess.Popen(["sudo","python3", "/home/capstone/csce483-capstone/src/hardware/midi_to_led_array.py", song_file])
        processRecord = subprocess.Popen(["python3", "/home/capstone/csce483-capstone/src/software/user_input/piano_to_midi.py", song_file])
        
        processLights.wait()
        processRecord.send_signal(signal.SIGINT)
        # Optionally, wait for both processes to complete if needed
        # process1.wait()
        # process2.wait()

        return jsonify({"status": "success", "message": f"Playing song {song_index}!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Error playing song: {str(e)}"}), 500


# def take_input():
#     try:
#         subprocess.run(["python3", "diddy.py"], check=True)
#         return "taking user input"
#     except subprocess.CalledProcessError as e:
#         return "error: "+e

@app.route("/currentlyplaying")
def playing():
    song_name = request.args.get('song_name')
    # song_duration = request.args.get('song_duration')
    # print(song_duration)
    # print(type(song_duration))
    SONG_PATH = midi_reference_path(song_name)
    midi_data = pretty_midi.PrettyMIDI(SONG_PATH)
    #midi_data = pretty_midi.PrettyMIDI('songs/'+song_name)
    duration = (midi_data.get_end_time())
    def get_bpm(path):
        mid = mido.MidiFile(path)
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                    bpm = mido.tempo2bpm(tempo)
                    return bpm
        return None
    duration += ((1/(get_bpm(SONG_PATH)/60))/4 )*50
    # Convert duration to mm:ss format
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    duration_formatted = f"{minutes:02}:{seconds:02}"  # Format as mm:ss
    return render_template("currentlyplaying.html",song_name=song_name,song_duration=f"{duration:.2f}", song_duration_formatted=duration_formatted)
    

@app.route("/stats")
def stats():
    global song_file
    import string
    # Name of MIDI files
    midi_reference = midi_reference_path(str(song_file))
    #midi_reference = "songs/"+str(song_file)
    midi_user = "/home/capstone/csce483-capstone/src/software/UI/UserInputRecorded/user.mid"
    print("midi_reference: ", midi_reference)
    
    # Calculate total accuracy and accuracy by notes
    total_acc = total_accuracy(midi_reference, midi_user)
    acc_by_notes = generate_by_note_stat(midi_reference, midi_user)
    return render_template("stats.html", song_data=song_file, total_accuracy=total_acc, accuracy_by_notes=acc_by_notes)

def midi_reference_path():
    global song_file
    midi_file_path = "/home/capstone/csce483-capstone/songs/"+str(song_file)
    return midi_file_path

if __name__ == "__main__":
    app.run(debug=True)
