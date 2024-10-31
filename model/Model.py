from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Float, Boolean
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
    total_tile_cost = Column(Float, default=tile_cost_per_sqft*tiling_area)
    total_flooring_cost = Column(Float, default=flooring_cost_per_sqft*surface_area)
    total_remodel_cost = Column(Float)

    supply = relationship("Supply")


class Supply(Base):
    __tablename__ = 'supplies'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    name = Column(String)
    quantity = Column(Integer)
    cost_per_item = Column(Float)
    total_supply_cost = Column(Float, default=quantity*cost_per_item)

    room = relationship("Room")


Base.metadata.create_all(engine)
