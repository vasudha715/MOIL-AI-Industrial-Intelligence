"""
Database tables for MOIL AI.
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    # roles: "industrialist", "geologist", "admin"
    role = Column(String, default="industrialist")
    created_at = Column(DateTime, default=datetime.utcnow)

    mines = relationship("Mine", back_populates="owner")


class Mine(Base):
    __tablename__ = "mines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location_name = Column(String, nullable=False)  # e.g. "Balaghat, Madhya Pradesh"
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="mines")
    exploration_results = relationship("ExplorationResult", back_populates="mine")


class ExplorationResult(Base):
    __tablename__ = "exploration_results"

    id = Column(Integer, primary_key=True, index=True)
    mine_id = Column(Integer, ForeignKey("mines.id"), nullable=True)
    location = Column(String)
    weather_risk = Column(Text)      # stored as JSON string
    satellite = Column(Text)         # stored as JSON string
    total_zones = Column(Integer)
    priority_summary = Column(Text)  # stored as JSON string
    top_zones = Column(Text)         # stored as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    mine = relationship("Mine", back_populates="exploration_results")


class ProductionTarget(Base):
    """Approved production targets, entered by the industrialist/admin.
    Until these are entered, shortfall analysis stays 'pending' (as flagged
    in the original M3 workbook)."""
    __tablename__ = "production_targets"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, unique=True, index=True)  # e.g. "2026-01"
    target_tonnes = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    mine_id = Column(Integer, ForeignKey("mines.id"), nullable=True)
    type = Column(String)       # e.g. "Shortfall", "Weather", "High Risk"
    severity = Column(String)   # "low", "medium", "high"
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
