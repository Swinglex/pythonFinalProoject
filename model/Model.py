from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Float, Boolean, Computed
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

engine = create_engine('sqlite:///house')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surface_area = Column(Float)
    flooring_type = Column(String)
    flooring_cost_per_sqft = Column(Float)

    is_tiling_needed = Column(Boolean)
    tile_type = Column(String)
    tile_cost_per_sqft = Column(Float)
    tiling_area = Column(Float)
    total_tile_cost = Column(Float)
    total_flooring_cost = Column(Float)
    total_remodel_cost = Column(Float)

    supply = relationship("Supply")

    def __init__(self, name, surface_area, flooring_type, flooring_cost_per_sqft, is_tiling_needed, tile_type,
                 tile_cost_per_sqft, tiling_area):
        self.name = name
        self.surface_area = surface_area
        self.flooring_type = flooring_type
        self.flooring_cost_per_sqft = flooring_cost_per_sqft
        self.is_tiling_needed = is_tiling_needed
        self.tile_type = tile_type
        self.tile_cost_per_sqft = tile_cost_per_sqft
        self.tiling_area = tiling_area
        self.total_tile_cost = tile_cost_per_sqft*tiling_area
        self.total_flooring_cost = flooring_cost_per_sqft*surface_area
        self.total_remodel_cost = self.total_tile_cost + self.total_flooring_cost




class Supply(Base):
    __tablename__ = 'supplies'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    name = Column(String)
    quantity = Column(Integer)
    cost_per_item = Column(Float)
    total_supply_cost = Column(Float)
    room = relationship("Room")

    def __init__(self, room_id, name, quantity, cost_per_item):
        self.name = name
        self.room_id = room_id
        self.quantity = quantity
        self.cost_per_item = cost_per_item
        self.total_supply_cost = quantity * cost_per_item



Base.metadata.create_all(engine)
