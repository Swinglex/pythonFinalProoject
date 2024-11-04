from flask import Flask, render_template, request, redirect, url_for, session
from model.Model import *
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)
app.secret_key = "woah"

sess = Session()
os.makedirs('static', exist_ok=True)


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

        # this checks the boolean of the form, it asks if it is true and returns it
        tiling = 'tiling' in request.form

        if tiling:
            tile_type = request.form['tile_type']
            tile_cost_per_sqft = float(request.form['tile_per_foot'])
            tiling_area = float(request.form['tile_area'])
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


        in_room = Room(name=room_name, surface_area=surface_area, flooring_type=flooring_type, flooring_cost_per_sqft=flooring_cost_per_sqft,
                       is_tiling_needed=tiling, tile_type=tile_type, tile_cost_per_sqft=tile_cost_per_sqft, tiling_area=tiling_area)
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

        in_supply = Supply(room_id=int(room_id), name=supply_name, quantity=int(quantity), cost_per_item=float(cost_per_item))

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
        if cost.total_supply_cost is None:
            continue
        sum_supply += cost.total_supply_cost
    return sum_supply

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    rooms = sess.query(Room).all()
    room_names = [in_room.name for in_room in rooms]
    remodel_costs = [in_room.total_remodel_cost for in_room in rooms]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=room_names, y=remodel_costs, palette="magma")
    plt.xlabel("Room Name")
    plt.ylabel("Remodel Cost")
    plt.title("Total Remodel Cost")

    img = os.path.join(app.root_path, 'static', "plot.png")
    plt.savefig(img)
    plt.close()

    return render_template("graph.html", plot_url=url_for('static', filename='plot.png'))


if __name__ == '__main__':
    app.run()

