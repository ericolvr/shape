"""user domain"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class User:
    """User Entity - Representa um user no dominio"""
    
    id: Optional[int] = None
    name: str
    email: str

    def validate(self) -> None:
        """Valida os campos do usuario"""
        if not self.name:
            raise ValueError("Name is required")
        if not self.email:
            raise ValueError("Email is required")
        if "@" not in self.email:
            raise ValueError("Invalid email format")
    
    
class UserRepository(ABC):
    """Interface para o repositório de usuarios"""
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Adiciona um usuario ao repositório"""
        pass

    @abstractmethod
    def list(self) -> List[User]:
        """Lista todos os usuarios do repositório"""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[User]:
        """Busca um usuario pelo id"""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Atualiza um usuario no repositório"""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Remove um usuario do repositório"""
        pass