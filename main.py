from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from flask import Flask, render_template, request, redirect, url_for

# Alchemy Does not need
# to be here, will be in model
engine = create_engine('sqlite:///house')
Session = sessionmaker(bind=engine)

Base = declarative_base()

app = Flask(__name__)
app.secretkey = 'woah'


@app.route('/')
def index():
    return render_template('HomePage.html')

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

