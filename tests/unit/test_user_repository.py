""" test repository  """
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.internal.core.domain.user import User
from app.internal.core.domain.exceptions import DuplicateEmailError, UserNotFoundError
from app.internal.infrastructure.database.models import Base, UserModel
from app.internal.infrastructure.database.user_repository import UserRepoImpl


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()


@pytest.fixture
def repository(db_session):
    return UserRepoImpl(db_session)


class TestUserRepository:
    def test_create_user_success(self, repository):
        user = User(name="João Silva", email="joao@example.com")

        created_user = repository.create(user)

        assert created_user.id is not None
        assert created_user.name == "João Silva"
        assert created_user.email == "joao@example.com"

    def test_create_user_duplicate_email(self, repository):
        user1 = User(name="João Silva", email="joao@example.com")
        repository.create(user1)

        user2 = User(name="Maria Santos", email="joao@example.com")

        with pytest.raises(DuplicateEmailError) as exc_info:
            repository.create(user2)

        assert "already exists" in str(exc_info.value)

    def test_list_users_empty(self, repository):
        users = repository.list()

        assert users == []

    def test_list_users_with_data(self, repository):
        user1 = User(name="João Silva", email="joao@example.com")
        user2 = User(name="Maria Santos", email="maria@example.com")

        repository.create(user1)
        repository.create(user2)

        users = repository.list()

        assert len(users) == 2
        assert users[0].name == "João Silva"
        assert users[1].name == "Maria Santos"

    def test_get_by_id_success(self, repository):
        user = User(name="João Silva", email="joao@example.com")
        created_user = repository.create(user)

        found_user = repository.get_by_id(created_user.id)

        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.name == "João Silva"
        assert found_user.email == "joao@example.com"

    def test_get_by_id_not_found(self, repository):
        found_user = repository.get_by_id(999)

        assert found_user is None

    def test_update_user_success(self, repository):
        user = User(name="João Silva", email="joao@example.com")
        created_user = repository.create(user)

        created_user.name = "João Silva Updated"
        created_user.email = "joao.updated@example.com"

        updated_user = repository.update(created_user)

        assert updated_user.id == created_user.id
        assert updated_user.name == "João Silva Updated"
        assert updated_user.email == "joao.updated@example.com"

    def test_update_user_not_found(self, repository):
        user = User(name="João Silva", email="joao@example.com", id=999)

        with pytest.raises(UserNotFoundError) as exc_info:
            repository.update(user)

        assert "not found" in str(exc_info.value)

    def test_update_user_duplicate_email(self, repository):
        user1 = User(name="João Silva", email="joao@example.com")
        user2 = User(name="Maria Santos", email="maria@example.com")

        created_user1 = repository.create(user1)
        repository.create(user2)

        created_user1.email = "maria@example.com"

        with pytest.raises(DuplicateEmailError) as exc_info:
            repository.update(created_user1)

        assert "already exists" in str(exc_info.value)

    def test_delete_user_success(self, repository):
        user = User(name="João Silva", email="joao@example.com")
        created_user = repository.create(user)

        result = repository.delete(created_user.id)

        assert result is True

        found_user = repository.get_by_id(created_user.id)
        assert found_user is None

    def test_delete_user_not_found(self, repository):
        result = repository.delete(999)

        assert result is False

    def test_create_user_persists_to_database(self, repository, db_session):
        user = User(name="João Silva", email="joao@example.com")
        created_user = repository.create(user)

        db_user = db_session.query(UserModel).filter_by(id=created_user.id).first()

        assert db_user is not None
        assert db_user.name == "João Silva"
        assert db_user.email == "joao@example.com"
        assert db_user.created_at is not None
        assert db_user.updated_at is not None
