"""
Configuración de la aplicación RetroArcade Hub
"""

# URL de conexión a la base de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./retroarcade.db"

# Configuración de la API
API_PREFIX = "/api/v1"
API_TITLE = "RetroArcade Hub API"
API_DESCRIPTION = """
🕹️ **RetroArcade Hub** - API gamificada para torneos de videojuegos retro

## Características principales:
- 🎮 **Gestión de torneos** de juegos clásicos
- 👤 **Perfiles de jugadores** con sistema de niveles
- ⚡ **Power-ups coleccionables** con efectos especiales  
- 🏆 **Rankings y puntuaciones** en tiempo real
- 💰 **Sistema de monedas** interno
- 🔐 **Autenticación JWT** (simulada en esta demo)

## Casos de uso implementados:
1. **Listar torneos disponibles** con filtros
2. **Crear perfil de jugador** con validaciones
3. **Aplicar power-ups** en torneos activos

## Tecnologías:
- FastAPI + SQLAlchemy + SQLite
- Testing con pytest
- Documentación automática con Swagger/OpenAPI
"""
API_VERSION = "1.0.0"

# Configuración de seguridad (simulada)
JWT_SECRET_KEY = "your-super-secret-jwt-key"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30