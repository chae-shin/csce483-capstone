from flask import Flask, render_template, request, redirect, url_for, jsonify
from songFilePickStats import song_data
import subprocess
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'songs/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    data = song_data()
    return render_template("index.html", song_data=data)

@app.route("/upload", methods=["POST"])
def upload_file():
    # checks if file chosen
    if 'filename' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    
    # file is chosen file
    file = request.files['filename']
    
    # is file name nothing
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400
    
    # if file perfect we add it to the folder
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        song_data()

        return jsonify({"status": "success", "message": "File uploaded successfully!", "file_path": file_path})


@app.route("/play_song", methods=["POST"])
def play_song():
    data = request.get_json()
    song_index = data.get("song_name")

    try:
        # Run the specific Python file based on the song index
        song_file = song_index # Adjust file path as needed
        print(song_file)
        subprocess.run(["python3", "RunningLights.py", song_file], check=True)
        return jsonify({"status": "success", "message": f"Playing song at index {song_index}!"})
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