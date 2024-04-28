from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello this is cat profile page <h1>Hello</h1>"