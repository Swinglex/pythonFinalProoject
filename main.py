from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
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
    if request.method == 'POST':
        #basics of the room
        room_name = request.form['room_name']
        surface_area = float(request.form['surface_area'])
        flooring_type = request.form['flooring_type']
        flooring_cost_per_sqft = float(request.form['flooring_cost_per_sqft'])

        # this checks the boolean of the form, it asks if it is true and returns it
        tiling = 'tiling' in request.form

        if tiling:
            tile_type = request.form['tile_type']
            tile_cost_per_sqft = float(request.form['tile_cost_per_sqft'])
            tiling_area = float(request.form['tiling_area'])
        else:
            tile_type = None
            tile_cost_per_sqft = None
            tiling_area = None

        #for tossing over to Supply and stuff
        session['room_order'] = {
            'room_name': room_name,
            'surface_area': surface_area,
            'flooring_type': flooring_type,
            'flooring_cost_per_sqft': flooring_cost_per_sqft,
            'tiling': tiling,
            'tile_type': tile_type,
            'tile_cost_per_sqft': tile_cost_per_sqft,
            'tiling_area': tiling_area
        }
    return render_template('/AddRoom.html')
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

        total_supply_cost = int(quantity) * float(cost_per_item)
        in_supply = Supply(name=supply_name, quantity=int(quantity), cost_per_item=float(cost_per_item), total_supply_cost=float(total_supply_cost))
        session.add(in_supply)
        session.commit()
    return render_template("AddSupply.html")

@app.route('/supplyDetails')
def supply_details():
    return render_template("SupplyDetails.html")

if __name__ == '__main__':
    app.run(debug=True)

