from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path

# Instância global do SQLAlchemy
db = SQLAlchemy()

# Instância global do LoginManager
login_manager = LoginManager()


def create_app():
    # Caminho raiz do repositório
    REPO_ROOT = Path(__file__).resolve().parents[3]

    app = Flask(
        __name__,
        template_folder=str(REPO_ROOT / "client" / "templates"),
        static_folder=str(REPO_ROOT / "client" / "static"),
    )

    # Configurações básicas
    app.config["SECRET_KEY"] = "your-secret-key-change-in-production"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializa extensões
    db.init_app(app)

    # Configura Flask-Login
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # Importa aqui pra evitar import circular
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registra blueprints
    from controllers.auth_controller import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.routes.tracker_routes import tracker_bp
    app.register_blueprint(tracker_bp)

    # Cria as tabelas no banco (inclui a tabela "user")
    with app.app_context():
        db.create_all()

    return app
