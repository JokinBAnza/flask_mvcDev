from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tu_clave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    db.init_app(app)
    login_manager.init_app(app)

    # Registrar blueprints
    from .blueprints.libros import libros_bp
    app.register_blueprint(libros_bp)
    
    return app
