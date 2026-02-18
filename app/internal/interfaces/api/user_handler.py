"""usr handlers"""
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from typing import List

from app.internal.core.services.user_service import UserService
from app.internal.core.domain.user import User
from app.internal.core.domain.exceptions import DuplicateEmailError, UserNotFoundError, ValidationError
from app.internal.interfaces.dto.user import UserRequest, UserUpdate, UserResponse
from app.internal.interfaces.api.dependencies import get_user_service
from app.internal.infrastructure.tasks.email_tasks import send_welcome_email
from app.config.logging import get_logger

logger = get_logger("api.user_handler")

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: UserRequest,
    background_tasks: BackgroundTasks,
    service: UserService = Depends(get_user_service)
):
    try:
        user = User(name=data.name, email=data.email)
        created_user = service.create(user)
        
        background_tasks.add_task(
            send_welcome_email, 
            created_user.email, 
            created_user.name
        )
        
        return created_user
    
    except DuplicateEmailError as e:
        logger.error(f"POST /users failed - duplicate email: {data.email}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=str(e)
        )
    except ValidationError as e:
        logger.error(f"POST /users failed - validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )


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
        logger.error(f"GET /users/{user_id} failed - not found")
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
    try:
        existing_user = service.get_by_id(user_id)
        if not existing_user:
            logger.error(f"PUT /users/{user_id} failed - not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        
        if data.name is not None:
            existing_user.name = data.name
        if data.email is not None:
            existing_user.email = data.email
        
        updated_user = service.update(existing_user)
        return updated_user

    except DuplicateEmailError as e:
        logger.error(f"PUT /users/{user_id} failed - duplicate email: {data.email}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=str(e)
        )
    except UserNotFoundError as e:
        logger.error(f"PUT /users/{user_id} failed - not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except ValidationError as e:
        logger.error(f"PUT /users/{user_id} failed - validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    success = service.delete(user_id)
    if not success:
        logger.error(f"DELETE /users/{user_id} failed - not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )