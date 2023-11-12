from flask import Flask, render_template, request, url_for, flash, redirect, abort

PORT = 5001

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    return render_template('index.html')

app.run(host="0.0.0.0", port=PORT)