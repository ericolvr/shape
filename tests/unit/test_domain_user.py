"""unit tests for User domain"""
import pytest
from app.internal.core.domain.user import User
from app.internal.core.domain.exceptions import ValidationError


class TestUserEntity:
    """Test User domain entity validation"""
    
    def test_create_valid_user(self):
        user = User(name="John Doe", email="john@example.com")
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.id is None
    
    def test_validate_success(self):
        user = User(name="John Doe", email="john@example.com")
        user.validate()
    
    def test_validate_empty_name(self):
        user = User(name="", email="john@example.com")
        with pytest.raises(ValidationError, match="Name is required"):
            user.validate()
    
    def test_validate_empty_email(self):
        user = User(name="John Doe", email="")
        with pytest.raises(ValidationError, match="Email is required"):
            user.validate()
    
    def test_validate_invalid_email_format(self):
        user = User(name="John Doe", email="invalid-email")
        with pytest.raises(ValidationError, match="Invalid email format"):
            user.validate()
    
    def test_user_with_id(self):
        
        user = User(id=1, name="John Doe", email="john@example.com")
        assert user.id == 1
