from flask import Flask, render_template, request, redirect, url_for, jsonify
from songFilePickStats import song_data
from Comparsion import total_accuracy, generate_by_note_stat
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    data = song_data()
    return render_template("index.html", song_data=data) 

@app.route("/play_song", methods=["POST"])
def play_song():
    try:
        # Run the specific Python file
        subprocess.run(["python3", "./midiFiles/hello_world_HCB.py"], check=True)
        return jsonify({"status": "success", "message": "Song is now playing!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Error playing song: {str(e)}"}), 500

@app.route("/currentlyplaying")
def playing():
    return render_template("currentlyplaying.html")

@app.route("/stats")
def stats():
    data = song_data()
    # Name of MIDI files
    midi_reference = "Happy_Birthday_Easy_to_play.mid"
    midi_user = "user.mid"
    # Calculate total accuracy and accuracy by notes
    total_acc = total_accuracy(midi_reference, midi_user)
    acc_by_notes = generate_by_note_stat(midi_reference, midi_user)
    return render_template("stats.html", song_data=data, total_accuracy=total_acc, accuracy_by_notes=acc_by_notes)

if __name__ == "__main__":
    app.run(debug=True)