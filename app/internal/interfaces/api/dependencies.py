""" dependencies injections """
from fastapi import Depends
from sqlalchemy.orm import Session

from app.internal.infrastructure.database.connection import get_db
from app.internal.infrastructure.database.user_repository import UserRepoImpl
from app.internal.core.services.user_service import UserService


def get_user_repository(db: Session = Depends(get_db)) -> UserRepoImpl:
    return UserRepoImpl(db)


def get_user_service(
    repo: UserRepoImpl = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repo=repo)
