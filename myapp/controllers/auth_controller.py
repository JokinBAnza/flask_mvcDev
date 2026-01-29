# myapp/controllers/auth_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from myapp import db
from myapp.services.hashPassword import hash_password, verify_password


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    from myapp.models.user import Usuario
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            flash("Debes rellenar todos los campos", "danger")
        elif Usuario.query.filter_by(username=username).first():
            flash("El usuario ya existe", "danger")
        else:
            hashed = hash_password(password)  # <- uso del servicio
            user = Usuario(username=username, password=hashed)
            db.session.add(user)
            db.session.commit()
            flash("Usuario registrado correctamente", "success")
            return redirect(url_for("auth.login"))
    
    return render_template("paginas/auth/register.html")


# ────────────── LOGIN ──────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    from myapp.models.user import Usuario
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Usuario.query.filter_by(username=username).first()
        if not user or not verify_password(password, user.password):  # <- aquí usamos el servicio
            flash("Usuario o contraseña incorrectos", "danger")
        else:
            login_user(user)
            flash("Has iniciado sesión correctamente", "success")
            return redirect(url_for("navigation.inicio"))
    return render_template("paginas/auth/login.html")


# ────────────── LOGOUT ──────────────
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión", "success")
    return redirect(url_for("navigation.inicio"))
