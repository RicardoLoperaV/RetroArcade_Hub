"""
Router para endpoints relacionados con torneos
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db import get_db
from ..models import Tournament
from ..schemas import TournamentResponse

router = APIRouter(
    prefix="/tournaments",
    tags=["tournaments"],
    responses={404: {"description": "No encontrado"}},
)

@router.get("", response_model=List[TournamentResponse])
async def list_tournaments(
    game_title: Optional[str] = None,
    status: str = "active",
    db: Session = Depends(get_db)
):
    """
    Listar torneos disponibles con filtros opcionales
    
    - **game_title**: Filtrar por juego específico
    - **status**: upcoming, active, completed
    """
    query = db.query(Tournament)
    
    if game_title:
        query = query.filter(Tournament.game_title.ilike(f"%{game_title}%"))
    
    if status:
        query = query.filter(Tournament.status == status)
    
    tournaments = query.all()
    
    # Agregar conteo de participantes actuales
    result = []
    for tournament in tournaments:
        tournament_dict = tournament.__dict__.copy()
        tournament_dict["current_participants"] = len(tournament.participants)
        result.append(TournamentResponse(**tournament_dict))
    
    return result