from flask import Flask, render_template, request, redirect, url_for, jsonify
from songFilePickStats import song_data
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
    return render_template("stats.html")

if __name__ == "__main__":
    app.run(debug=True)