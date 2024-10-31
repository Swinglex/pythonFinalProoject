from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from flask import Flask, render_template, request, redirect, url_for, session

engine = create_engine('sqlite:///house')
Session = sessionmaker(bind=engine)

Base = declarative_base()

app = Flask(__name__)
app.secretkey = 'woah'


class Room:
    pass


@app.route('/', methods=['GET', 'POST'])
def index(session=None):
    rooms = session.query(Room).all()
    return render_template('index.html', rooms=rooms)

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    name = request.form.get('name')
    surface_area = request.form.get('surface_area', type=float)
    flooring_type = request.form.get('flooring_type')
    flooring_cost_per_sqft = request.form.get('flooring_cost_per_sqft', type=float)

   #ToDO build out.
    is_tiling_needed = bool(request.form.get('is_tiling_needed'))
    tile_type = request.form.get('tile_type')
    tile_cost_per_sqft = request.form.get('tile_cost_per_sqft', type=float)
    tiling_area = request.form.get('tiling_area', type=float)

    total_flooring_cost = surface_area * flooring_cost_per_sqft
    total_tile_cost = tiling_area * tile_cost_per_sqft if is_tiling_needed else 0
    total_remodel_cost = total_flooring_cost + total_tile_cost

    new_room = Room(
        name=name,
        surface_area=surface_area,
        flooring_type=flooring_type,
        flooring_cost_per_sqft=flooring_cost_per_sqft,
        is_tiling_needed=is_tiling_needed,
        tile_type=tile_type,
        tile_cost_per_sqft=tile_cost_per_sqft,
        tiling_area=tiling_area,
        total_tile_cost=total_tile_cost,
        total_flooring_cost=total_flooring_cost,
        total_remodel_cost=total_remodel_cost
        )
    session.add(new_room)
    session.commit()

    return redirect(url_for('index'))
return render_template('add_room.html')

@app.route('/roomDetails')
def details():
    return

@app.route('supply')
def supply():
    return

@app.route('/supplyDetails')
def details():
    return

