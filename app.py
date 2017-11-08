from flask import render_template

from src.api import EphemAPI

app, api = EphemAPI.create_flask_app(__name__)

@app.route("/")
def home():
    return render_template("index.html")
