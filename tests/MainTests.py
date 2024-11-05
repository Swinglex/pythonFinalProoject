# test_app.py
import pytest
from main import app, sess
from model.Model import Supply


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_approute(client):
    responseIndex = client.get('/')
    responseRoom = client.get('/room')
    responseSupply = client.get('/supply')

    assert responseIndex.status_code == 200
    assert responseRoom.status_code == 200
    assert responseSupply.status_code == 200

def test_room(client):
    response = client.post('/room', data={
        'room_name': 'CoolRoom',
        'surface_area': '20.0',
        'flooring_type': 'marble',
        'cost_per_foot': '2.5',
        'tiling': 'on',
        'tile_type': 'ceramic',
        'tile_per_foot': '3.0',
        'tile_area': '15.0'
    })

    #we redirect the details on room on the same page
    assert response.status_code == 302

    with client.session_transaction() as session:
        assert session['room_order']['room_name'] == 'CoolRoom'
        assert session['room_order']['surface_area'] == 20.0
        assert session['room_order']['flooring_type'] == 'marble'
        assert session['room_order']['tiling'] is True
        assert session['room_order']['tile_type'] == 'ceramic'
        assert session['room_order']['tile_cost_per_sqft'] == 3.0
        assert session['room_order']['tiling_area'] == 15.0

def test_supply(client):
    room_id = 1

    response = client.post('/supply', data={
        'supply_name': 'Paint',
        'quantity': '5',
        'cost_per_item': '20.0',
        'room_id': room_id
    })
    assert response.status_code == 302

    #tests the database rather than the session
    supply = sess.query(Supply).filter_by(name='Paint', room_id=room_id).first()
    assert supply is not None
    assert supply.name == 'Paint'
    assert supply.quantity == 5
    assert supply.cost_per_item == 20.0
    assert supply.room_id == room_id




