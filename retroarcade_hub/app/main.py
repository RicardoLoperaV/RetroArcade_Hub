"""
Punto de entrada principal para la API RetroArcade Hub
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import json
from datetime import datetime, timedelta

from .db import engine, SessionLocal
from .models import Base, PowerUp, Tournament
from .config import API_TITLE, API_DESCRIPTION, API_VERSION, API_PREFIX
from .routers import players, tournaments, power_ups, auth

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Función para crear datos de ejemplo en el evento de inicio
async def create_sample_data():
    """Crear datos de ejemplo para testing"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existen datos
        if db.query(Tournament).first():
            return
        
        # Crear power-ups de ejemplo
        power_ups_data = [
            {
                "name": "Speed Boost",
                "description": "Aumenta la velocidad del jugador por 30 minutos",
                "effect_type": "speed_boost",
                "effect_value": 1.5,
                "duration_minutes": 30,
                "rarity": "common",
                "price": 100
            },
            {
                "name": "Super Shield",
                "description": "Protección total contra ataques por 15 minutos",
                "effect_type": "shield",
                "effect_value": 1.0,
                "duration_minutes": 15,
                "rarity": "rare",
                "price": 250
            },
            {
                "name": "Damage Multiplier",
                "description": "Duplica el daño de todos los ataques",
                "effect_type": "damage_up",
                "effect_value": 2.0,
                "duration_minutes": 20,
                "rarity": "epic",
                "price": 500
            }
        ]
        
        for pu_data in power_ups_data:
            power_up = PowerUp(**pu_data)
            db.add(power_up)
        
        # Crear torneos de ejemplo
        tournaments_data = [
            {
                "name": "Pac-Man Championship 2025",
                "game_title": "Pac-Man",
                "description": "Torneo clásico del come-cocos más famoso",
                "entry_fee": 50,
                "prize_pool": 5000,
                "max_participants": 32,
                "start_date": datetime.utcnow() + timedelta(days=1),
                "end_date": datetime.utcnow() + timedelta(days=3),
                "status": "upcoming"
            },
            {
                "name": "Street Fighter II Legends",
                "game_title": "Street Fighter II",
                "description": "Combates épicos con los luchadores legendarios",
                "entry_fee": 100,
                "prize_pool": 10000,
                "max_participants": 16,
                "start_date": datetime.utcnow() - timedelta(hours=2),
                "end_date": datetime.utcnow() + timedelta(days=2),
                "status": "active"
            },
            {
                "name": "Tetris Speed Masters",
                "game_title": "Tetris",
                "description": "¿Quién es el más rápido armando líneas?",
                "entry_fee": 25,
                "prize_pool": 2500,
                "max_participants": 64,
                "start_date": datetime.utcnow() + timedelta(hours=6),
                "end_date": datetime.utcnow() + timedelta(days=1),
                "status": "upcoming"
            }
        ]
        
        for tournament_data in tournaments_data:
            tournament = Tournament(**tournament_data)
            db.add(tournament)
        
        db.commit()
        print("✅ Datos de ejemplo creados exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando datos de ejemplo: {e}")
        db.rollback()
    finally:
        db.close()

# Lifespan para manejar eventos de inicio y cierre
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al iniciar la aplicación
    await create_sample_data()
    yield
    # Código que se ejecuta al cerrar la aplicación
    pass

# Crear la aplicación FastAPI
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir los routers
app.include_router(players.router, prefix=API_PREFIX)
app.include_router(tournaments.router, prefix=API_PREFIX)
app.include_router(power_ups.router, prefix=API_PREFIX)
app.include_router(auth.router, prefix=API_PREFIX)

# Ruta raíz
@app.get("/")
async def root():
    return {
        "message": "Bienvenido a RetroArcade Hub API",
        "docs": "/docs",
        "version": API_VERSION
    }

# Punto de entrada para ejecutar la aplicación directamente
if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando RetroArcade Hub API...")
    print("📖 Documentación disponible en: http://localhost:8000/docs")
    print("🧪 Ejecutar tests: pytest -v tests/")
    uvicorn.run("retroarcade_hub.app.main:app", host="0.0.0.0", port=8000, reload=True)