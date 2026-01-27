from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  # solo se define aquí

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///python.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-secret-key"

    db.init_app(app)

    # Importar modelos aquí **después** de db.init_app
    from .models.libro import Libro
    from .models.socio import Socio

    # Registrar blueprints
    from .controllers.navigation_controller import navigation_bp
    app.register_blueprint(navigation_bp)
    from .controllers.libros_controller import libros_bp
    app.register_blueprint(libros_bp)
    from .controllers.api_controller import api_bp
    app.register_blueprint(api_bp)
    from .controllers.socios_controller import socios_bp 
    app.register_blueprint(socios_bp)

    # Crear tablas en la base de datos
    with app.app_context():
        db.create_all()

    return app
