
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from app.models.libro import Libro
from app.models.socio import Socio


db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///python.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # evitar warning de SQLAlchemy
     # 🔐 CLAVE SECRETA (obligatoria para Flask-WTF)
    app.config["SECRET_KEY"] = "dev-secret-key"  # luego la convendría cambiarla por una más segura en producción

    db.init_app(app)

    # Registro de los Blueprints
    from app.controllers.navigation_controller import navigation_bp
    app.register_blueprint(navigation_bp)
    from app.controllers.libros_controller import libros_bp
    app.register_blueprint(libros_bp)
    from app.controllers.api_controller import api_bp
    app.register_blueprint(api_bp)
        # Crear las tablas en la base de datos
    with app.app_context():
        db.create_all()

    return app
