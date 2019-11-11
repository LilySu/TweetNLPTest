from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")

def hello():
    return render_template('home.html')

@app.route("/about")

def preds():
    return render_template('about.html')