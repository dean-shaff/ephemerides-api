from flask import Flask, render_template

from src.api import EphemAPI

api = EphemAPI()
app = Flask(__name__)

@app.route("/get_ephem")
def get_ephem():
    pass

@app.route("/")
def home():
    return render_template("index.html")
