# TODO: Routes need to be moved to app/routes

from flask import Flask, render_template
from pathlib import Path    # For handling file paths

REPO_ROOT = Path(__file__).resolve().parents[3] # TEMPORARY FOR TESTING. Ideally, backend should act as an API

app = Flask(__name__, template_folder=str(REPO_ROOT / 'client' / 'templates')) # Create an instance of the Flask class

@app.route("/") # Decorator to tell Flask what URL should trigger the function
def home():
    return render_template('tracker/media_list.html')