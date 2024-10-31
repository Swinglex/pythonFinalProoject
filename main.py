from flask import Flask, render_template, request, redirect, url_for
from model.Model import *
app = Flask(__name__)
app.secretkey = 'woah'


@app.route('/')
def index():
    session = Session()
    rooms = session.query(Room).all()
    return render_template('index.html', room = rooms)

@app.route('/room')
def room():
    return render_template("AddRoom.html")

@app.route('/roomDetails')
def room_details():
    return render_template("RoomDetails.html")

@app.route('/supply')
def supply():
    return render_template("AddSupply.html")

@app.route('/supplyDetails')
def supply_details():
    return render_template("SupplyDetails.html")

if __name__ == '__main__':
    app.run(debug=True)

