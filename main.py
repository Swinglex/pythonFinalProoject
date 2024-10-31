from flask import Flask, render_template, request, redirect, url_for
from model.Model import *
app = Flask(__name__)
app.secretkey = 'woah'
session = Session()

@app.route('/')
def index():
    rooms = session.query(Room).all()
    return render_template('index.html', room = rooms)

@app.route('/room', methods=['GET', 'POST'])
def room():
    return render_template("AddRoom.html")

@app.route('/roomDetails')
def room_details():
    return render_template("RoomDetails.html")

@app.route('/supply', methods=['GET', 'POST'])
def supply():
    if request.method == "POST":
        supply_name = request.form['supply_name']
        quantity = request.form['quantity']
        cost_per_item = request.form['cost_per_item']

        in_supply = Supply(name=supply_name, quantity=int(quantity), cost_per_item=float(cost_per_item))
        session.add(in_supply)
        session.commit()
    return render_template("AddSupply.html")

@app.route('/supplyDetails')
def supply_details():
    return render_template("SupplyDetails.html")

if __name__ == '__main__':
    app.run(debug=True)

