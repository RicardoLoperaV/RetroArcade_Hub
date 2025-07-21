"""
Router para endpoints relacionados con power-ups
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from ..models import PowerUp
from ..schemas import PowerUpResponse

router = APIRouter(
    prefix="/power-ups",
    tags=["power-ups"],
    responses={404: {"description": "No encontrado"}},
)

@router.get("", response_model=List[PowerUpResponse])
async def list_power_ups(db: Session = Depends(get_db)):
    """Listar todos los power-ups disponibles en el marketplace"""
    power_ups = db.query(PowerUp).all()
    return power_ups