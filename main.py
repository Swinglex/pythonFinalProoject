from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from flask import Flask, render_template, request, redirect, url_for

engine = create_engine('sqlite:///house')
Session = sessionmaker(bind=engine)

Base = declarative_base()

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

