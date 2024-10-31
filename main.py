from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secretkey = 'woah'


@app.route('/')
def index():
    return render_template('/')

@app.route('/AddRoom', methods=['GET', 'POST'])
def addroom():
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

@app.route('/roomDetails')
def details():
    return

@app.route('supply')
def supply():
    return

@app.route('/supplyDetails')
def details():
    return

