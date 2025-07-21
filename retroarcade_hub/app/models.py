"""
Modelos SQLAlchemy para RetroArcade Hub
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .db import Base

class Player(Base):
    """Modelo para jugadores"""
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    avatar_url = Column(String(200), default="https://retro.com/avatars/default.png")
    coins = Column(Integer, default=1000)
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    tournament_participations = relationship("TournamentParticipation", back_populates="player")
    power_ups = relationship("PlayerPowerUp", back_populates="player")

class Tournament(Base):
    """Modelo para torneos"""
    __tablename__ = "tournaments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    game_title = Column(String(100), nullable=False)
    description = Column(String(500))
    entry_fee = Column(Integer, default=0)
    prize_pool = Column(Integer, default=0)
    max_participants = Column(Integer, default=32)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(20), default="upcoming")  # upcoming, active, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    participants = relationship("TournamentParticipation", back_populates="tournament")

class PowerUp(Base):
    """Modelo para power-ups"""
    __tablename__ = "power_ups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    effect_type = Column(String(30))  # speed_boost, damage_up, shield, etc.
    effect_value = Column(Float)  # multiplicador o valor del efecto
    duration_minutes = Column(Integer, default=30)
    rarity = Column(String(20), default="common")  # common, rare, epic, legendary
    price = Column(Integer, default=100)
    
    # Relaciones
    player_power_ups = relationship("PlayerPowerUp", back_populates="power_up")

class PlayerPowerUp(Base):
    """Modelo para la relación entre jugadores y power-ups (inventario)"""
    __tablename__ = "player_power_ups"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    power_up_id = Column(Integer, ForeignKey("power_ups.id"))
    quantity = Column(Integer, default=1)
    acquired_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    player = relationship("Player", back_populates="power_ups")
    power_up = relationship("PowerUp", back_populates="player_power_ups")

class TournamentParticipation(Base):
    """Modelo para la participación de jugadores en torneos"""
    __tablename__ = "tournament_participations"
    
    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    player_id = Column(Integer, ForeignKey("players.id"))
    score = Column(Integer, default=0)
    position = Column(Integer)
    active_power_ups = Column(String(200))  # JSON string de power-ups activos
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    tournament = relationship("Tournament", back_populates="participants")
    player = relationship("Player", back_populates="tournament_participations")