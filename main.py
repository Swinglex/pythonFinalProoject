from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from sqlalchemy import func
from model.validation import *

from model.Model import *
import matplotlib.pyplot as plt
import seaborn as sns
import os

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
        vals = []
        room_name = request.form['room_name']
        surface_area, val_surf_area = float_val(request.form['surface_area'])
        if not val_surf_area:
            flash("Surface Area Must Be a Number")
            vals.append(val_surf_area)
        flooring_type = request.form['flooring_type']
        flooring_cost_per_sqft, val_cost_per = float_val(request.form['cost_per_foot'])
        if not val_cost_per:
            flash("Flooring Cost Per Foot Must Be a Number")
            vals.append(val_cost_per)

        tiling = 'tiling' in request.form

        if tiling:
            tile_type = request.form['tile_type']
            tile_cost_per_sqft, val_tile_cost = float_val(request.form['tile_per_foot'])
            if not val_tile_cost:
                flash("Tile Cost Per Foot Must Be a Number")
                vals.append(val_tile_cost)
            tiling_area, val_tile_area = float_val(request.form['tile_area'])
            if not val_tile_area:
                flash("Tile Area Must Be a Number")
                vals.append(val_tile_area)
        else:
            tile_type = None
            tile_cost_per_sqft = 0
            tiling_area = 0

        if False in vals:
            return redirect(url_for('room'))

        in_room = Room(name=room_name, surface_area=surface_area, flooring_type=flooring_type, flooring_cost_per_sqft=flooring_cost_per_sqft,
                       is_tiling_needed=tiling, tile_type=tile_type, tile_cost_per_sqft=tile_cost_per_sqft, tiling_area=tiling_area)
        sess.add(in_room)
        sess.commit()
        return redirect(url_for('index'))
    else:
        return render_template('add_room.html')


@app.route('/roomDetails')
def room_details():
    detail_room_id = request.args['room_id']
    detail_room = sess.query(Room).filter(Room.id == int(detail_room_id)).first()
    detail_supplies = sess.query(Supply).filter(Supply.room_id==int(detail_room_id)).all()

    return render_template("RoomDetails.html", room=detail_room, supplies=detail_supplies)

@app.route('/editRoom', methods=['GET', 'POST'])
def room_edit():
    if request.method == 'POST':
        vals = []
        room_name = request.form['room_name']
        surface_area, val_surf_area = float_val(request.form['surface_area'])
        if not val_surf_area:
            flash("Surface Area Must Be a Number")
            vals.append(val_surf_area)
        flooring_type = request.form['flooring_type']
        flooring_cost_per_sqft, val_cost_per = float_val(request.form['cost_per_foot'])
        if not val_cost_per:
            flash("Flooring Cost Per Foot Must Be a Number")
            vals.append(val_cost_per)

        tiling = 'tiling' in request.form

        if tiling:
            tile_type = request.form['tile_type']
            tile_cost_per_sqft, val_tile_cost = float_val(request.form['tile_per_foot'])
            if not val_tile_cost:
                flash("Tile Cost Per Foot Must Be a Number")
                vals.append(val_tile_cost)
            tiling_area, val_tile_area = float_val(request.form['tile_area'])
            if not val_tile_area:
                flash("Tile Area Must Be a Number")
                vals.append(val_tile_area)
        else:
            tile_type = None
            tile_cost_per_sqft = 0
            tiling_area = 0

        if False in vals:
            return redirect(url_for('room_edit'))

        room_id = int(request.args['room_id'])
        sess.query(Room).filter(Room.id == room_id).update({Room.name: room_name, Room.surface_area: surface_area, Room.flooring_type: flooring_type,
                                                                 Room.flooring_cost_per_sqft: flooring_cost_per_sqft, Room.is_tiling_needed: tiling, Room.tile_type: tile_type,
                                                                 Room.tile_cost_per_sqft: tile_cost_per_sqft, Room.tiling_area: tiling_area})
        sess.commit()
        return redirect(url_for('index'))
    else:
        room_id = int(request.args['room_id'])
        room_detail = sess.query(Room).filter(Room.id == room_id).first()

        return render_template("EditRoom.html", room=room_detail)

@app.route('/supply', methods=['GET', 'POST'])
def supply():
    if request.method == 'POST':
        vals = []
        supply_name = request.form['supply_name']
        quantity = int(request.form['quantity'])
        cost_per_item, val_cost = float_val(request.form['cost_per_item'])
        if not val_cost:
            flash("Cost Per Item Must Be a Number")
            vals.append(val_cost)

        room_name = request.form['room_name']

        room_id = name_to_room(room_name)

        if room_id is None:
            flash("Room Not Found")
            vals.append(False)

        if False in vals:
            return redirect(url_for('supply'))

        in_supply = Supply(room_id=int(room_id.id), name=supply_name, quantity=int(quantity), cost_per_item=float(cost_per_item))

        sess.add(in_supply)
        sess.commit()
        sess.query(Room).filter_by(id=int(room_id.id)).update(
            {Room.total_remodel_cost: Room.total_flooring_cost + Room.total_tile_cost + sum_supplies(int(room_id.id))})
        sess.commit()
        return redirect(url_for('index'))
    else:
        return render_template("AddSupply.html")


@app.route('/editSupply', methods=['GET', 'POST'])
def supply_edit():
    if request.method == 'POST':
        vals = []
        supply_id = int(request.args['supply_id'])
        supply_name = request.form['supply_name']
        supply_quantity = int(request.form['quantity'])
        supply_cost_per_item, val_cost = float_val(request.form['cost_per_item'])
        if not val_cost:
            flash("Cost Per Item Must Be a Number")
            vals.append(val_cost)

        room_name = request.form['room_name']

        room_id = name_to_room(room_name)

        if room_id is None:
            flash("Room Not Found")
            vals.append(False)

        if False in vals:
            return redirect(f"/editSupply?supply_id={supply_id}")

        sess.query(Supply).filter(Supply.id == supply_id).update(
            {Supply.name: supply_name, Supply.quantity: supply_quantity, Supply.cost_per_item: supply_cost_per_item,
             Supply.room_id: room_id.id})
        sess.commit()

        return redirect(url_for('index'))
    else:
        supply_id = int(request.args['supply_id'])
        supplycool = sess.query(Supply).join(Room).filter(Supply.id == supply_id).first()
        return render_template("EditSupply.html", supply=supplycool)


def sum_supplies(room_id):
    total_supplies = sess.query(Supply).filter(Supply.room_id == room_id).all()
    sum_supply = 0
    for cost in total_supplies:
        if cost.total_supply_cost is None:
            continue
        sum_supply += cost.total_supply_cost
    return sum_supply


def name_to_room(room_name):
    supply_room = sess.query(Room).filter(func.lower(Room.name) == room_name.lower()).first()
    if supply_room is None:
        return None
    return supply_room


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    os.makedirs('static', exist_ok=True)
    rooms = sess.query(Room).all()
    room_names = [in_room.name for in_room in rooms]
    remodel_costs = [in_room.total_remodel_cost for in_room in rooms]

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

