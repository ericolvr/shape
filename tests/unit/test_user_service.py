"""unit tests for UserService"""
import pytest
from unittest.mock import Mock
from app.internal.core.services.user_service import UserService
from app.internal.core.domain.user import User
from app.internal.core.domain.exceptions import ValidationError, DuplicateEmailError


class TestUserService:
    def test_create_user_success(self):
        mock_repo = Mock()
        mock_repo.create.return_value = User(id=1, name="John Doe", email="john@example.com")

        service = UserService(mock_repo)
        user = User(name="John Doe", email="john@example.com")

        result = service.create(user)

        assert result.id == 1
        assert result.name == "John Doe"
        mock_repo.create.assert_called_once_with(user)

    def test_create_user_validation_error(self):
        mock_repo = Mock()
        service = UserService(mock_repo)
        user = User(name="", email="john@example.com")

        with pytest.raises(ValidationError):
            service.create(user)

        mock_repo.create.assert_not_called()

    def test_create_user_duplicate_email(self):
        mock_repo = Mock()
        mock_repo.create.side_effect = DuplicateEmailError("Email already exists")

        service = UserService(mock_repo)
        user = User(name="John Doe", email="john@example.com")

        with pytest.raises(DuplicateEmailError):
            service.create(user)

    def test_list_users(self):
        mock_repo = Mock()
        mock_repo.list.return_value = [
            User(id=1, name="John Doe", email="john@example.com"),
            User(id=2, name="Jane Doe", email="jane@example.com"),
        ]

        service = UserService(mock_repo)
        users = service.list()

        assert len(users) == 2
        assert users[0].name == "John Doe"
        mock_repo.list.assert_called_once()

    def test_get_by_id(self):
        mock_repo = Mock()
        mock_repo.get_by_id.return_value = User(id=1, name="John Doe", email="john@example.com")

        service = UserService(mock_repo)
        user = service.get_by_id(1)

        assert user.id == 1
        mock_repo.get_by_id.assert_called_once_with(1)

    def test_update_user_success(self):
        mock_repo = Mock()
        mock_repo.update.return_value = User(id=1, name="John Updated", email="john@example.com")

        service = UserService(mock_repo)
        user = User(id=1, name="John Updated", email="john@example.com")

        result = service.update(user)

        assert result.name == "John Updated"
        mock_repo.update.assert_called_once_with(user)

    def test_delete_user(self):
        mock_repo = Mock()
        mock_repo.delete.return_value = True

        service = UserService(mock_repo)
        result = service.delete(1)

        assert result is True
        mock_repo.delete.assert_called_once_with(1)
