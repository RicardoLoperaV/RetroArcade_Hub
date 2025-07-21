# RetroArcade Hub API

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.23-orange.svg)
![Status](https://img.shields.io/badge/Status-Development-yellow.svg)

API gamificada para torneos de videojuegos retro con sistema de power-ups y perfiles de jugadores.

## 📋 Requisitos

- Python 3.8+
- Dependencias:
  - fastapi
  - uvicorn
  - sqlalchemy
  - pytest
  - python-multipart

## 💻 Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/yourusername/RetroArcade_Hub.git
   cd RetroArcade_Hub
   ```

2. Crear entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install fastapi uvicorn sqlalchemy pytest python-multipart
   ```

## 🚀 Ejecución

Para iniciar el servidor:

```bash
python RetroArcade_Hub.py
```

O alternativamente:

```bash
uvicorn RetroArcade_Hub:app --reload
```

La API estará disponible en: http://localhost:8000

Documentación Swagger UI: http://localhost:8000/docs

## 🎮 Ejemplos de uso

### 1. Crear jugador

```bash
curl -X POST "http://localhost:8000/api/v1/players" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "retromaster2025",
    "email": "master@retroarcade.com",
    "avatar_url": "https://retro.com/avatars/master.png"
  }'
```

### 2. Listar torneos activos

```bash
curl "http://localhost:8000/api/v1/tournaments?status=active"
```

### 3. Filtrar torneos por juego

```bash
curl "http://localhost:8000/api/v1/tournaments?game_title=Pac-Man"
```

### 4. Aplicar power-up (requiere autenticación)

```bash
curl -X POST "http://localhost:8000/api/v1/players/1/apply-power-up" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{
    "tournament_id": 1,
    "power_up_id": 1
  }'
```

### 5. Ver inventario de jugador

```bash
curl "http://localhost:8000/api/v1/players/1/inventory" \
  -H "Authorization: Bearer your-jwt-token"
```

### 6. Listar power-ups disponibles

```bash
curl "http://localhost:8000/api/v1/power-ups"
```

## 📊 Respuestas de ejemplo

### Jugador creado:
```json
{
  "id": 1,
  "username": "retromaster2025",
  "email": "master@retroarcade.com",
  "avatar_url": "https://retro.com/avatars/master.png",
  "coins": 1000,
  "level": 1,
  "experience_points": 0,
  "created_at": "2025-07-21T10:30:00",
  "is_active": true
}
```

### Torneo disponible:
```json
{
  "id": 1,
  "name": "Pac-Man Championship 2025",
  "game_title": "Pac-Man",
  "description": "Torneo clásico del come-cocos más famoso",
  "entry_fee": 50,
  "prize_pool": 5000,
  "max_participants": 32,
  "current_participants": 8,
  "start_date": "2025-07-22T10:00:00",
  "end_date": "2025-07-24T18:00:00",
  "status": "upcoming"
}
```

### Power-up aplicado:
```json
{
  "message": "Power-up 'Speed Boost' applied successfully",
  "effect": "speed_boost: +1.5",
  "duration_minutes": 30,
  "remaining_quantity": 2
}
```

## 🧪 Tests

Los tests están integrados en el archivo `RetroArcade_Hub.py` usando pytest. Para ejecutarlos:

```bash
pytest RetroArcade_Hub.py -v
```

Tests implementados:

- ✅ test_list_tournaments_success - Lista torneos correctamente
- ✅ test_list_tournaments_with_filters - Filtra por juego específico
- ✅ test_create_player_success - Crea jugador con coins iniciales
- ✅ test_create_player_duplicate_username_fails - Previene usernames duplicados
- ✅ test_create_player_invalid_email_fails - Valida formato de email
- ✅ test_apply_power_up_success - Aplica power-up exitosamente
- ✅ test_apply_power_up_insufficient_inventory_fails - Maneja inventario vacío

## 🏗️ Estructura del proyecto

```
RetroArcade_Hub/
├── RetroArcade_Hub.py    # Archivo principal con API y tests
├── README.md             # Documentación
└── .gitignore            # Archivos ignorados por git
```

## 🔧 Tecnologías utilizadas

- **FastAPI**: Framework web de alto rendimiento
- **SQLAlchemy**: ORM para interacción con base de datos
- **SQLite**: Base de datos para desarrollo
- **Pydantic**: Validación de datos y serialización
- **Pytest**: Framework de testing

## 🛡️ Seguridad implementada

1. **Autenticación JWT**: Tokens seguros para API (simulada)
2. **Validación de entrada**: Pydantic schemas con validaciones
3. **Sanitización SQL**: SQLAlchemy ORM previene inyección
4. **Manejo de errores**: Respuestas HTTP apropiadas

## 🚀 Casos de uso implementados

1. **Listar torneos disponibles** con filtros por juego y estado
2. **Crear perfil de jugador** con validaciones de datos
3. **Aplicar power-ups** en torneos activos con efectos temporales

## 📈 Funcionalidades planificadas

1. **Sistema de NFTs**: Coleccionables únicos de personajes retro
2. **Matchmaking inteligente**: Algoritmo de emparejamiento por skill
3. **Streaming en vivo**: Integración con Twitch para torneos
4. **Chat en tiempo real**: WebSocket para comunicación
5. **Marketplace**: Compra/venta de power-ups entre jugadores

## 🤝 Contribuir

1. Haz un fork del proyecto
2. Crea una rama para tu funcionalidad (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.