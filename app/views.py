from app import app
from flask import render_template

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/temp")
def temp():
    return "Temp"
