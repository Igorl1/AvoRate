from src.infra.db.database import db
from src.domain.user import User


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def to_entity(self):
        """
        Converts the Model (Database) to Entity (Domain)
        """
        return User(
            id=self.id, username=self.username, email=self.email, password=self.password
        )

    @staticmethod
    def from_entity(user_entity):
        """
        Converts Entity (Domain) to Model (Database)
        """
        return UserModel(
            id=user_entity.id,
            username=user_entity.username,
            email=user_entity.email,
            password=user_entity.password,
        )


class UserRepository:
    def get_user_by_email(self, email: str) -> User:
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            return user_model.to_entity()
        return None

    def get_user_by_id(self, user_id: int) -> User:
        user_model = UserModel.query.get(user_id)
        if user_model:
            return user_model.to_entity()
        return None

    def save_user(self, user: User) -> User:
        user_model = UserModel.from_entity(user)
        db.session.add(user_model)
        db.session.commit()
        user.id = user_model.id
        return user
