from io import BytesIO

import sns
from flask import Flask, render_template, request, redirect, url_for, session
from model.Model import *
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = "woah"

sess = Session()


@app.route('/')
def index():
    rooms = sess.query(Room).all()
    return render_template('index.html', rooms = rooms)

@app.route('/room', methods=['GET', 'POST'])
def room():
    if request.method == 'POST':
        #basics of the room
        room_name = request.form['room_name']
        surface_area = float(request.form['surface_area'])
        flooring_type = request.form['flooring_type']
        flooring_cost_per_sqft = float(request.form['cost_per_foot'])


        total_flooring_cost = (flooring_cost_per_sqft * surface_area)
        # this checks the boolean of the form, it asks if it is true and returns it
        tiling = 'tiling' in request.form

        if tiling:
            tile_type = request.form['tile_type']
            tile_cost_per_sqft = float(request.form['tile_per_foot'])
            tiling_area = float(request.form['tile_area'])
            total_tile_cost = (tile_cost_per_sqft * tiling_area)
        else:
            tile_type = None
            tile_cost_per_sqft = None
            tiling_area = None
            total_tile_cost = 0

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


        in_room = Room(name=room_name, surface_area=surface_area, flooring_type=flooring_type, flooring_cost_per_sqft=flooring_cost_per_sqft,
                       is_tiling_needed=tiling, tile_type=tile_type, tile_cost_per_sqft=tile_cost_per_sqft, tiling_area=tiling_area,
                       total_tile_cost=total_tile_cost, total_flooring_cost=total_flooring_cost,
                       total_remodel_cost=(total_tile_cost + total_flooring_cost))
        sess.add(in_room)
        sess.commit()
        return redirect(url_for('index'))

    return render_template('/add_room.html')


@app.route('/roomDetails')
def room_details():
    room_id = request.args.get('room_id')
    detail_room = sess.query(Room).filter(Room.id == int(room_id)).first()
    detail_supplies = sess.query(Supply).filter(Supply.room_id==int(room_id)).all()

    return render_template("RoomDetails.html", room=detail_room, supplies=detail_supplies)

@app.route('/supply', methods=['GET', 'POST'])
def supply():
    if request.method == "POST":
        supply_name = request.form['supply_name']
        quantity = request.form['quantity']
        cost_per_item = request.form['cost_per_item']
        room_id = request.form['room_id']

        total_supply_cost = int(quantity) * float(cost_per_item)
        in_supply = Supply(room_id=int(room_id), name=supply_name, quantity=int(quantity), cost_per_item=float(cost_per_item), total_supply_cost=float(total_supply_cost))

        sess.add(in_supply)
        sess.commit()
        sess.query(Room).filter_by(id=int(room_id)).update(
            {Room.total_remodel_cost: Room.total_flooring_cost + Room.total_tile_cost + sum_supplies(int(room_id))})
        sess.commit()
        return redirect(url_for('index'))

    return render_template("AddSupply.html")

@app.route('/supplyDetails')
def supply_details():
    return render_template("SupplyDetails.html")

def sum_supplies(room_id):
    total_supplies = sess.query(Supply).filter(Supply.room_id == room_id).all()
    sum_supply = 0
    for cost in total_supplies:
        sum_supply += cost.total_supply_cost
    return sum_supply

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    rooms = sess.query(Room).all()
    room_names = [room.name for room in rooms]
    remodel_costs = [room.total_remodel_cost for room in rooms]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=room_names, y=remodel_costs, palette="magma")
    plt.xlabel("Room Name")
    plt.ylabel("Remodel Cost")
    plt.title("Total Remodel Cost")

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return render_template("graph.html", plot_url=plot_url)
if __name__ == '__main__':
    app.run()

