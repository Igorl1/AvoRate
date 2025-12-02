from flask import Flask
from flask_login import LoginManager
from pathlib import Path
from src.infra.db.database import db

# Global instance of LoginManager
login_manager = LoginManager()


def create_app():
    # Repository root path
    REPO_ROOT = Path(__file__).resolve().parents[3]

    app = Flask(
        __name__,
        template_folder=str(REPO_ROOT / "client" / "templates"),
        static_folder=str(REPO_ROOT / "client" / "static"),
    )

    # Basic configurations
    app.config["SECRET_KEY"] = "your-secret-key-change-in-production"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Configure Flask-Login
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from src.infra.repositories.user_repository import UserRepository

    user_repo = UserRepository()

    @login_manager.user_loader
    def load_user(user_id):
        return user_repo.get_user_by_id(int(user_id))

    # Register blueprints
    from .routes.auth_routes import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .routes.tracker_routes import tracker_bp

    app.register_blueprint(tracker_bp)

    # Create tables in the database (includes the 'user' table)
    with app.app_context():
        db.create_all()

    return app
