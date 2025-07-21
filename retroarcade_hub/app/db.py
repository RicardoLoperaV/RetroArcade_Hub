"""
Configuración de la base de datos para RetroArcade Hub
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import SQLALCHEMY_DATABASE_URL

# Crear el motor de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Solo necesario para SQLite
)

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la clase base para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión de BD
def get_db():
    """
    Dependencia para obtener una sesión de base de datos.
    Se utiliza con Depends() en los endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()