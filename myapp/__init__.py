from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()  # solo se define aquí
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Ruta a la página de login

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///python.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-secret-key"

    db.init_app(app)
    login_manager.init_app(app)

    # Importar modelos aquí **después** de db.init_app
    from .models.libro import Libro
    from .models.socio import Socio
    from .models.user import Usuario  # tu modelo de usuarios
    from .models.prestamo import Prestamo

    # Registrar blueprints
    from .controllers.navigation_controller import navigation_bp
    app.register_blueprint(navigation_bp)
    from .controllers.libros_controller import libros_bp
    app.register_blueprint(libros_bp)
    from .controllers.api_controller import api_bp
    app.register_blueprint(api_bp)
    from .controllers.socios_controller import socios_bp 
    app.register_blueprint(socios_bp)
    from .controllers.auth_controller import auth_bp  # tu nuevo auth blueprint
    app.register_blueprint(auth_bp)

    # Crear tablas en la base de datos
    with app.app_context():
        db.create_all()

    return app

# Usuario loader para Flask-Login
from .models.user import Usuario

@login_manager.user_loader
def load_user(user_id):
    from .models.user import Usuario
    return Usuario.query.get(int(user_id))

