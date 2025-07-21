"""
Router para endpoints relacionados con jugadores
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from ..models import Player, PlayerPowerUp, PowerUp, TournamentParticipation
from ..schemas import PlayerCreate, PlayerResponse
from .auth import get_current_player
import json
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/players",
    tags=["players"],
    responses={404: {"description": "No encontrado"}},
)

@router.post("", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
async def create_player(player_data: PlayerCreate, db: Session = Depends(get_db)):
    """
    Crear nuevo perfil de jugador
    
    - **username**: Único, 3-50 caracteres
    - **email**: Formato válido, único
    - **avatar_url**: Opcional, URL del avatar
    
    El jugador inicia con 1000 coins y nivel 1
    """
    # Verificar username único
    if db.query(Player).filter(Player.username == player_data.username).first():
        raise HTTPException(
            status_code=400,
            detail=f"Username '{player_data.username}' already exists"
        )
    
    # Verificar email único
    if db.query(Player).filter(Player.email == player_data.email).first():
        raise HTTPException(
            status_code=400,
            detail=f"Email '{player_data.email}' already exists"
        )
    
    # Crear jugador con valores por defecto
    db_player = Player(
        username=player_data.username,
        email=player_data.email,
        avatar_url=player_data.avatar_url or "https://retro.com/avatars/default.png",
        coins=1000,  # Coins iniciales
        level=1,
        experience_points=0
    )
    
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    
    return db_player

@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: int, db: Session = Depends(get_db)):
    """Obtener perfil de jugador por ID"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.post("/{player_id}/apply-power-up")
async def apply_power_up(
    player_id: int,
    power_up_data: dict,
    current_player=Depends(get_current_player),
    db: Session = Depends(get_db)
):
    """
    Aplicar power-up a torneo específico
    
    - **tournament_id**: ID del torneo activo
    - **power_up_id**: ID del power-up a aplicar
    
    Requiere autenticación y que el jugador tenga el power-up en inventario
    """
    # Verificar que el jugador existe y es el actual
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player or player.id != current_player["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Verificar que el torneo existe y está activo
    tournament = db.query(Tournament).filter(
        Tournament.id == power_up_data["tournament_id"],
        Tournament.status == "active"
    ).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Active tournament not found")
    
    # Verificar que el jugador tiene el power-up en inventario
    player_power_up = db.query(PlayerPowerUp).filter(
        PlayerPowerUp.player_id == player_id,
        PlayerPowerUp.power_up_id == power_up_data["power_up_id"],
        PlayerPowerUp.quantity > 0
    ).first()
    
    if not player_power_up:
        raise HTTPException(status_code=400, detail="Power-up not available in inventory")
    
    # Obtener detalles del power-up
    power_up = db.query(PowerUp).filter(PowerUp.id == power_up_data["power_up_id"]).first()
    if not power_up:
        raise HTTPException(status_code=404, detail="Power-up not found")
    
    # Verificar participación en torneo
    participation = db.query(TournamentParticipation).filter(
        TournamentParticipation.tournament_id == power_up_data["tournament_id"],
        TournamentParticipation.player_id == player_id
    ).first()
    
    if not participation:
        raise HTTPException(status_code=400, detail="Player not registered in tournament")
    
    # Aplicar power-up
    # 1. Consumir power-up del inventario
    player_power_up.quantity -= 1
    if player_power_up.quantity == 0:
        db.delete(player_power_up)
    
    # 2. Agregar power-up activo a la participación del torneo
    active_power_ups = json.loads(participation.active_power_ups or "[]")
    active_power_ups.append({
        "power_up_id": power_up.id,
        "name": power_up.name,
        "effect_type": power_up.effect_type,
        "effect_value": power_up.effect_value,
        "applied_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(minutes=power_up.duration_minutes)).isoformat()
    })
    participation.active_power_ups = json.dumps(active_power_ups)
    
    db.commit()
    
    return {
        "message": f"Power-up '{power_up.name}' applied successfully",
        "effect": f"{power_up.effect_type}: +{power_up.effect_value}",
        "duration_minutes": power_up.duration_minutes,
        "remaining_quantity": player_power_up.quantity if player_power_up else 0
    }

@router.get("/{player_id}/inventory")
async def get_player_inventory(
    player_id: int,
    current_player=Depends(get_current_player),
    db: Session = Depends(get_db)
):
    """Obtener inventario de power-ups del jugador"""
    if player_id != current_player["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    inventory = db.query(PlayerPowerUp, PowerUp).join(PowerUp).filter(
        PlayerPowerUp.player_id == player_id,
        PlayerPowerUp.quantity > 0
    ).all()
    
    result = []
    for player_pu, power_up in inventory:
        result.append({
            "power_up": power_up,
            "quantity": player_pu.quantity,
            "acquired_at": player_pu.acquired_at
        })
    
    return result