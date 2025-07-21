"""
Script para ejecutar la aplicación RetroArcade Hub
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando RetroArcade Hub API...")
    print("📖 Documentación disponible en: http://localhost:8000/docs")
    print("🧪 Ejecutar tests: pytest -v retroarcade_hub/tests/")
    uvicorn.run("retroarcade_hub.app.main:app", host="0.0.0.0", port=8000, reload=True)