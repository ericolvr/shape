""" user repository """
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.internal.core.domain.user import User, UserRepository
from app.internal.core.domain.exceptions import DuplicateEmailError, UserNotFoundError
from app.internal.infrastructure.database.models import UserModel
from app.config.logging import get_logger

logger = get_logger("infrastructure.user_repository")


class UserRepoImpl(UserRepository):
    """ user repository implementation """
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        db_user = UserModel(
            name=user.name,
            email=user.email,
        )
        self.db.add(db_user)
        try:
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Database integrity error on user creation: email={user.email}, error={str(e)}")
            if "unique constraint" in str(e).lower() or "duplicate key" in str(e).lower():
                raise DuplicateEmailError(f"Email '{user.email}' already exists")
            raise
        
        return self._to_entity(db_user)

    def list(self) -> List[User]:
        users = self.db.query(UserModel).all()
        return [self._to_entity(user) for user in users]
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        return self._to_entity(user)

    def update(self, user: User) -> User:
        db_user = self.db.query(UserModel).filter(
            UserModel.id == user.id
        ).with_for_update().first()
        if not db_user:
            logger.error(f"User not found for update: id={user.id}")
            raise UserNotFoundError(f"User with id {user.id} not found")
        
        db_user.name = user.name
        db_user.email = user.email
        
        try:
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Database integrity error on user update: id={user.id}, error={str(e)}")
            if "unique constraint" in str(e).lower() or "duplicate key" in str(e).lower():
                raise DuplicateEmailError(f"Email '{user.email}' already exists")
            raise

        return self._to_entity(db_user)

    def delete(self, user_id: int) -> bool:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return False
        
        try:
            self.db.delete(user)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting user from database: id={user_id}, error={str(e)}")
            raise
        
        return True

    def _to_entity(self, user: UserModel) -> User:
        return User(
            id=user.id,
            name=user.name,
            email=user.email,
        )
        