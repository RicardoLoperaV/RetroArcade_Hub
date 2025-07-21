# RetroArcade Hub API

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.23-orange.svg)
![Status](https://img.shields.io/badge/Status-Development-yellow.svg)

RetroArcade Hub API es un backend RESTful construido en Python 3.8+ con FastAPI 0.104.1 y SQLAlchemy 2.0.23 sobre SQLite, diseñado para recrear la experiencia de un centro de juegos arcade clásico en la web. Ofrece gestión completa de perfiles de jugadores (niveles, estadísticas y validaciones Pydantic), organización de torneos de títulos retro, un sistema de power‑ups y economía interna con monedas virtuales. Incorpora autenticación JWT ligera, documentación automática vía Swagger/OpenAPI y una suite de pruebas con pytest para asegurar calidad y fiabilidad. Con esta plataforma, desarrolladores y entusiastas disponen de un back‑end modular, de rápida implantación y altamente extensible, que resuelve la necesidad de prototipar y desplegar mecánicas de gamificación desde el registro de usuarios y resultados hasta la asignación de recompensas, facilitando la integración con front‑ends interactivos y la expansión ágil con nuevos juegos o funcionalidades.


## 📋 Requisitos

- Python 3.8+
- Dependencias:
  - fastapi
  - uvicorn[standard]
  - sqlalchemy
  - pydantic
  - python-multipart
  - pytest

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
   pip install -r requirements.txt
   ```

## 🚀 Ejecución

Para iniciar el servidor:

```bash
python run.py
```

O alternativamente:

```bash
uvicorn retroarcade_hub.app.main:app --reload
```

La API estará disponible en: http://localhost:8000

Documentación Swagger UI: http://localhost:8000/docs

## 🏗️ Estructura del proyecto

```
RetroArcade_Hub/
├── retroarcade_hub/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # Punto de entrada de la aplicación
│   │   ├── config.py         # Configuración de la aplicación
│   │   ├── db.py             # Configuración de la base de datos
│   │   ├── models.py         # Modelos SQLAlchemy
│   │   ├── schemas.py        # Esquemas Pydantic
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── auth.py       # Autenticación
│   │       ├── players.py    # Endpoints de jugadores
│   │       ├── tournaments.py # Endpoints de torneos
│   │       └── power_ups.py  # Endpoints de power-ups
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_retroarcade.py # Tests de la API
│   └── __init__.py
├── run.py                    # Script para ejecutar la aplicación
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación
```

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

## 🧪 Tests

Para ejecutar los tests:

```bash
pytest -v retroarcade_hub/tests/
```

Tests implementados:

- ✅ test_list_tournaments_success - Lista torneos correctamente
- ✅ test_list_tournaments_with_filters - Filtra por juego específico
- ✅ test_create_player_success - Crea jugador con coins iniciales
- ✅ test_create_player_duplicate_username_fails - Previene usernames duplicados
- ✅ test_create_player_invalid_email_fails - Valida formato de email
- ✅ test_apply_power_up_success - Aplica power-up exitosamente
- ✅ test_apply_power_up_insufficient_inventory_fails - Maneja inventario vacío

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