from flask import Flask, render_template, request, jsonify
from songFilePickStats import song_data
import subprocess
import os
import diddy
from Comparsion import total_accuracy, generate_by_note_stat

app = Flask(__name__)

UPLOAD_FOLDER = 'songs/'
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

    try:
        # Run the specific Python file based on the song index
        song_file = song_index  # Adjust file path as needed
        print(song_file)
        # subprocess.run(["python3", "RunningLights.py", song_file], check=True)
        # subprocess.run(["python3", "diddy.py", song_file], check=True)
        
        # Popen should run the processes in parallel
        subprocess.Popen(["python3", "RunningLights.py", song_file])
        subprocess.Popen(["python3", "diddy.py", song_file])
        
        # Optionally, wait for both processes to complete if needed
        process1.wait()
        process2.wait()

        return jsonify({"status": "success", "message": f"Playing song {song_index}!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Error playing song: {str(e)}"}), 500


def take_input():
    try:
        subprocess.run(["python3", "diddy.py"], check=True)
        return "taking user input"
    except subprocess.CalledProcessError as e:
        return "error: "+e

@app.route("/currentlyplaying")
def playing():
    return render_template("currentlyplaying.html")

@app.route("/stats")
def stats():
    global song_file

    # Name of MIDI files
    midi_reference = song_file
    midi_user = "user.mid"
    print("midi_reference: ", midi_reference)
    
    # Calculate total accuracy and accuracy by notes
    total_acc = total_accuracy(midi_reference, midi_user)
    acc_by_notes = generate_by_note_stat(midi_reference, midi_user)
    return render_template("stats.html", song_data=song_file, total_accuracy=total_acc, accuracy_by_notes=acc_by_notes)

if __name__ == "__main__":
    app.run(debug=True)
