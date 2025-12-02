from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Business rules for the User. Flask-Login requires these properties."""

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
        """Flask-Login needs the ID as a string."""
        return str(self.id)
