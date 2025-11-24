from src.infra.config import db
from src.core.entities.user import User

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def to_entity(self):
        """Converte o Modelo (Banco) para Entidade (Core)"""
        return User(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password
        )
    
    @staticmethod
    def from_entity(user_entity):
        """Converte Entidade (Core) para Modelo (Banco)"""
        return UserModel(
            id=user_entity.id,
            username=user_entity.username,
            email=user_entity.email,
            password=user_entity.password
        )