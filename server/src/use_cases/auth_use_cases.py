from werkzeug.security import generate_password_hash, check_password_hash
from src.domain.user import User
from src.infra.repositories.user_repository import UserRepository


class AuthUseCases:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def login(self, email: str, password: str) -> User:
        user = self.user_repo.get_user_by_email(email)
        if user and check_password_hash(user.password, password):
            return user
        return None

    def signup(self, email: str, name: str, password: str) -> User:
        existing_user = self.user_repo.get_user_by_email(email)
        if existing_user:
            raise ValueError("Email already exists")
        hashed_password = generate_password_hash(password)
        user = User(username=name, email=email, password=hashed_password)
        return self.user_repo.save_user(user)
