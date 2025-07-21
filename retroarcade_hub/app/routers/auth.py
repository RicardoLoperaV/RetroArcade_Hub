"""
Router para autenticación y autorización
"""

from fastapi import Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "No encontrado"}},
)

security = HTTPBearer()

# Mock de autenticación (en producción usar JWT real)
def get_current_player(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependencia para obtener el jugador actual autenticado.
    En una implementación real, validaría el token JWT y retornaría el jugador.
    """
    # En implementación real, validar JWT y retornar player actual
    return {"id": 1, "username": "test_player"}