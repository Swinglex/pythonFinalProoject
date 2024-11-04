import pytest

from main import supply
from model.Model import Room, Supply


class TestModel:
    @pytest.fixture
    def models_room(self):
        from model.Model import Room
        return Room(name="Bathroom", surface_area=25.50, flooring_type="Wood", flooring_cost_per_sqft=5.50,
                    is_tiling_needed=True, tile_type="Marble", tile_cost_per_sqft=10.50, tiling_area=15.25)

    @pytest.fixture
    def models_supply(self):
        from model.Model import Supply
        return Supply(name="Chair", room_id=1, quantity=2, cost_per_item=2.5)

    def test_room(self, models_room):
        assert isinstance(models_room, Room)

    def test_supply(self, models_supply):
        assert isinstance(models_supply, Supply)

    def test_room_data(self, models_room):
        assert models_room.name == "Bathroom"
        assert models_room.surface_area == 25.50
        assert models_room.flooring_type == "Wood"
        assert models_room.flooring_cost_per_sqft == 5.50
        assert models_room.is_tiling_needed
        assert models_room.tile_type == "Marble"
        assert models_room.tile_cost_per_sqft == 10.5
        assert models_room.tiling_area == 15.25

        assert models_room.total_tile_cost == 160.125
        assert models_room.total_flooring_cost == 140.25
        assert models_room.total_remodel_cost == 300.375

    def test_supply_data(self, models_supply):
        assert models_supply.name == "Chair"
        assert models_supply.room_id == 1
        assert models_supply.quantity == 2
        assert models_supply.cost_per_item == 2.5

        assert models_supply.total_supply_cost == 5



