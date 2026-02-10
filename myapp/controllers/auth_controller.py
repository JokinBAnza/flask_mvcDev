# myapp/controllers/auth_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from myapp.services.user_service import crear_usuario, autenticar_usuario, existe_usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ────────────── REGISTER ──────────────
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Debes rellenar todos los campos", "danger")
        elif existe_usuario(username, password):
            # Si ya existe el usuario, `autenticar_usuario` devolverá True (o el objeto Usuario si cambiaste la función)
            flash("El usuario ya existe", "danger")
        else:
            crear_usuario(username=username, password=password)
            flash("Usuario registrado correctamente", "success")
            return redirect(url_for("auth.login"))

    return render_template("paginas/auth/register.html")


# ────────────── LOGIN ──────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = autenticar_usuario(username, password)  # devuelve Usuario o None
        if not user:
            flash("Usuario o contraseña incorrectos", "danger")
        else:
            login_user(user)
            return redirect(url_for("navigation.inicio"))

    return render_template("paginas/auth/login.html")


# ────────────── LOGOUT ──────────────
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("navigation.inicio"))
