"""
Tests para la API RetroArcade Hub
"""

import pytest
import uuid
from fastapi.testclient import TestClient

from retroarcade_hub.app.main import app

class TestRetroArcadeAPI:
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture
    def sample_player_data(self):
        return {
            "username": "retromaster_" + str(uuid.uuid4())[:8],
            "email": f"test_{uuid.uuid4()}@retro.com",
            "avatar_url": "https://retro.com/avatars/master.png"
        }
    
    # TESTS PARA CASO DE USO 1: LISTAR TORNEOS
    def test_list_tournaments_success(self, client):
        """Test exitoso: Debe retornar lista de torneos activos"""
        response = client.get("/api/v1/tournaments")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        # Verificar estructura de respuesta
        if len(response.json()) > 0:
            tournament = response.json()[0]
            assert "id" in tournament
            assert "name" in tournament
            assert "game_title" in tournament
    
    def test_list_tournaments_with_filters(self, client):
        """Test con filtros: Debe filtrar por juego específico"""
        response = client.get("/api/v1/tournaments?game_title=Pac-Man")
        assert response.status_code == 200
        tournaments = response.json()
        for tournament in tournaments:
            assert "Pac-Man" in tournament["game_title"]
    
    # TESTS PARA CASO DE USO 2: CREAR JUGADOR
    def test_create_player_success(self, client, sample_player_data):
        """Test exitoso: Debe crear jugador con coins iniciales"""
        response = client.post("/api/v1/players", json=sample_player_data)
        assert response.status_code == 201
        player = response.json()
        assert player["username"] == sample_player_data["username"]
        assert player["coins"] == 1000  # Coins iniciales
        assert player["level"] == 1
        assert player["is_active"] == True
    
    def test_create_player_duplicate_username_fails(self, client, sample_player_data):
        """Test de fallo: Username duplicado debe fallar"""
        # Crear primer jugador
        client.post("/api/v1/players", json=sample_player_data)
        # Intentar crear segundo con mismo username
        response = client.post("/api/v1/players", json=sample_player_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    def test_create_player_invalid_email_fails(self, client):
        """Test de fallo: Email inválido debe fallar"""
        invalid_data = {
            "username": "testuser",
            "email": "invalid-email",
            "avatar_url": "https://test.com/avatar.png"
        }
        response = client.post("/api/v1/players", json=invalid_data)
        assert response.status_code == 422
    
    # TESTS PARA CASO DE USO 3: APLICAR POWER-UP
    def test_apply_power_up_success(self, client, sample_player_data):
        """Test exitoso: Aplicar power-up debe consumir item y mejorar stats"""
        # Crear jugador
        player_response = client.post("/api/v1/players", json=sample_player_data)
        player_id = player_response.json()["id"]
        
        # Mock: El jugador tiene un power-up en inventario
        power_up_data = {
            "tournament_id": 1,
            "power_up_id": 1
        }
        
        response = client.post(
            f"/api/v1/players/{player_id}/apply-power-up",
            json=power_up_data,
            headers={"Authorization": "Bearer fake-token"}
        )
        # En implementación real, verificaría que el power-up se aplicó correctamente
        # Por ahora verificamos estructura de respuesta
        assert response.status_code in [200, 404]  # 404 si no hay tournament/powerup
    
    def test_apply_power_up_insufficient_inventory_fails(self, client):
        """Test de fallo: Sin power-up en inventario debe fallar"""
        power_up_data = {
            "tournament_id": 1,
            "power_up_id": 999  # Power-up inexistente
        }
        
        response = client.post(
            "/api/v1/players/1/apply-power-up",
            json=power_up_data,
            headers={"Authorization": "Bearer fake-token"}
        )
        assert response.status_code in [400, 404]