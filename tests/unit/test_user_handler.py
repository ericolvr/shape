""" test api handlers """
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock

from app.main import app
from app.internal.core.domain.user import User
from app.internal.core.domain.exceptions import (
    DuplicateEmailError,
    ValidationError,
)
from app.internal.interfaces.api.dependencies import get_user_service


@pytest.fixture
def mock_user_service():
    return Mock()


@pytest.fixture
def client(mock_user_service):
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestUserHandlers:
    def test_create_user_success(self, client, mock_user_service):
        mock_user_service.create.return_value = User(
            id=1, name="João Silva", email="joao@example.com"
        )

        response = client.post("/users/", json={"name": "João Silva", "email": "joao@example.com"})

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "João Silva"
        assert data["email"] == "joao@example.com"
        mock_user_service.create.assert_called_once()

    def test_create_user_duplicate_email(self, client, mock_user_service):
        mock_user_service.create.side_effect = DuplicateEmailError(
            "Email 'joao@example.com' already exists"
        )

        response = client.post("/users/", json={"name": "João Silva", "email": "joao@example.com"})

        assert response.status_code == 409
        data = response.json()
        assert "already exists" in data["detail"]

    def test_create_user_validation_error(self, client, mock_user_service):
        mock_user_service.create.side_effect = ValidationError("Invalid email format")

        response = client.post("/users/", json={"name": "João Silva", "email": "invalid-email"})

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_create_user_invalid_payload(self, client):
        response = client.post("/users/", json={"name": "Jo"})

        assert response.status_code == 422

    def test_list_users_success(self, client, mock_user_service):
        mock_user_service.list.return_value = [
            User(id=1, name="João Silva", email="joao@example.com"),
            User(id=2, name="Maria Santos", email="maria@example.com"),
        ]

        response = client.get("/users/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "João Silva"
        assert data[1]["name"] == "Maria Santos"
        mock_user_service.list.assert_called_once()

    def test_list_users_empty(self, client, mock_user_service):
        mock_user_service.list.return_value = []

        response = client.get("/users/")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_user_by_id_success(self, client, mock_user_service):
        mock_user_service.get_by_id.return_value = User(
            id=1, name="João Silva", email="joao@example.com"
        )

        response = client.get("/users/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "João Silva"
        mock_user_service.get_by_id.assert_called_once_with(1)

    def test_get_user_by_id_not_found(self, client, mock_user_service):
        mock_user_service.get_by_id.return_value = None

        response = client.get("/users/999")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_update_user_success(self, client, mock_user_service):
        mock_user_service.get_by_id.return_value = User(
            id=1, name="João Silva", email="joao@example.com"
        )
        mock_user_service.update.return_value = User(
            id=1, name="João Updated", email="joao.updated@example.com"
        )

        response = client.put(
            "/users/1", json={"name": "João Updated", "email": "joao.updated@example.com"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "João Updated"
        assert data["email"] == "joao.updated@example.com"
        mock_user_service.update.assert_called_once()

    def test_update_user_not_found(self, client, mock_user_service):
        mock_user_service.get_by_id.return_value = None

        response = client.put(
            "/users/999", json={"name": "João Updated", "email": "joao.updated@example.com"}
        )

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]

    def test_update_user_duplicate_email(self, client, mock_user_service):
        mock_user_service.get_by_id.return_value = User(
            id=1, name="João Silva", email="joao@example.com"
        )
        mock_user_service.update.side_effect = DuplicateEmailError("Email already exists")

        response = client.put("/users/1", json={"name": "João Silva", "email": "maria@example.com"})

        assert response.status_code == 409
        data = response.json()
        assert "already exists" in data["detail"]

    def test_update_user_validation_error(self, client, mock_user_service):
        mock_user_service.get_by_id.return_value = User(
            id=1, name="João Silva", email="joao@example.com"
        )
        mock_user_service.update.side_effect = ValidationError("Invalid email format")

        response = client.put("/users/1", json={"name": "João Silva", "email": "invalid"})

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_update_user_partial(self, client, mock_user_service):
        mock_user_service.get_by_id.return_value = User(
            id=1, name="João Silva", email="joao@example.com"
        )
        mock_user_service.update.return_value = User(
            id=1, name="João Updated", email="joao@example.com"
        )

        response = client.put("/users/1", json={"name": "João Updated"})

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "João Updated"
        assert data["email"] == "joao@example.com"

    def test_delete_user_success(self, client, mock_user_service):
        mock_user_service.delete.return_value = True

        response = client.delete("/users/1")

        assert response.status_code == 204
        mock_user_service.delete.assert_called_once_with(1)

    def test_delete_user_not_found(self, client, mock_user_service):
        mock_user_service.delete.return_value = False

        response = client.delete("/users/999")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]
