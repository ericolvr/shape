"""usr handlers"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.internal.core.services.user_service import UserService
from app.internal.core.domain.user import User
from app.internal.interfaces.dto.user import UserRequest, UserUpdate, UserResponse
from app.internal.interfaces.api.dependencies import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: UserRequest,
    service: UserService = Depends(get_user_service)
):
    user = User(name=data.name, email=data.email)
    created_user = service.create(user)
    return created_user


@router.get("/", response_model=List[UserResponse])
def list_all(service: UserService = Depends(get_user_service)):
    return service.list()


@router.get("/{user_id}", response_model=UserResponse)
def get_by_id(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    existing_user = service.get_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    if data.name:
        existing_user.name = data.name
    if data.email:
        existing_user.email = data.email
    
    updated_user = service.update(existing_user)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    success = service.delete(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )