"""
Esquemas Pydantic para validación y serialización de datos
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Esquemas para Jugadores
class PlayerCreate(BaseModel):
    """Esquema para crear un nuevo jugador"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+')
    avatar_url: Optional[str] = None

class PlayerResponse(BaseModel):
    """Esquema para respuesta de jugador"""
    id: int
    username: str
    email: str
    avatar_url: str
    coins: int
    level: int
    experience_points: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

# Esquemas para Torneos
class TournamentResponse(BaseModel):
    """Esquema para respuesta de torneo"""
    id: int
    name: str
    game_title: str
    description: str
    entry_fee: int
    prize_pool: int
    max_participants: int
    current_participants: int
    start_date: datetime
    end_date: datetime
    status: str
    
    class Config:
        from_attributes = True

# Esquemas para Power-ups
class PowerUpApplication(BaseModel):
    """Esquema para aplicar un power-up"""
    tournament_id: int
    power_up_id: int

class PowerUpResponse(BaseModel):
    """Esquema para respuesta de power-up"""
    id: int
    name: str
    description: str
    effect_type: str
    effect_value: float
    duration_minutes: int
    rarity: str
    price: int
    
    class Config:
        from_attributes = True