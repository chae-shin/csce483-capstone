from flask import Flask, render_template, request, redirect, url_for
from songFilePickStats import song_data

app = Flask(__name__)

@app.route("/")
def home():
    data = song_data()
    return render_template("index.html", song_data=data)    

@app.route("/currentlyplaying")
def playing():
    return render_template("currentlyplaying.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

if __name__ == "__main__":
    app.run(debug=True)