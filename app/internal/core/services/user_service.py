""" user service """
from typing import List, Optional
from app.internal.core.domain.user import User, UserRepository


class UserService:
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def create(self, user: User) -> User:
        user.validate()
        return self.user_repo.create(user)
    
    def list(self) -> List[User]:
        return self.user_repo.list()

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repo.get_by_id(user_id)

    def update(self, user: User) -> User:
        user.validate()
        return self.user_repo.update(user)

    def delete(self, id: int) -> bool:
        return self.user_repo.delete(id)