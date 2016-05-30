from app import app

@app.route("/")
def hello():
    return "Hello World"

@app.route("/temp")
def temp():
    return "Temp"
