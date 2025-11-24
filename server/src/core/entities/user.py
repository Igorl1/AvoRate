from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    """Regras de negócio do Usuário."""
    username: str
    email: str
    password: str  
    id: Optional[int] = None
        
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        """O Flask-Login precisa recuperar o ID como string"""
        return str(self.id)