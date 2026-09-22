from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from .base import Base

class Intersection(Base):
    __tablename__ = "intersections"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    lat = Column(Float)
    lng = Column(Float)

class Road(Base):
    __tablename__ = "roads"
    
    id = Column(String, primary_key=True, index=True)
    source_id = Column(String)
    target_id = Column(String)
    capacity = Column(Integer)
    length = Column(Float)

class SignalDecision(Base):
    __tablename__ = "signal_decisions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    intersection_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    selected_phase = Column(String)
    duration = Column(Integer)
    reason = Column(String)

class Metric(Base):
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    avg_waiting_time = Column(Float)
    max_queue_length = Column(Integer)
    throughput = Column(Integer)
    spillback_events = Column(Integer)
