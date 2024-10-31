from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secretkey = 'woah'


@app.route('/')
def index():
    return render_template('/')

@app.route('/room')
def room():
    return

@app.route('/roomDetails')
def details():
    return

@app.route('supply')
def supply():
    return

@app.route('/supplyDetails')
def details():
    return

