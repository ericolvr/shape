""" user repository """
from typing import List, Optional
from sqlalchemy.orm import Session

from app.internal.core.domain.user import User, UserRepository
from app.internal.infrastructure.database.models import UserModel


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
        self.db.commit()
        
        return self.to_entity(db_user)

    def list(self) -> List[User]:
        users = self.db.query(UserModel).all()
        return [self.to_entity(user) for user in users]
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        return self.to_entity(user)

    def update(self, user: User) -> User:
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not db_user:
            raise ValueError("User not found")
        
        db_user.name = user.name
        db_user.email = user.email
        
        self.db.commit()
        self.db.refresh(db_user)

        return self.to_entity(db_user)

    def delete(self, user_id: int) -> bool:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        
        return True

    def to_entity(self, user: UserModel) -> User:
        return User(
            id=user.id,
            name=user.name,
            email=user.email,
        )
        