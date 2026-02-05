# myapp/controllers/socios_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from myapp.forms.socio_form import SocioForm
from myapp.services.socio_service import (
    crear_socio,
    obtener_todos_los_socios,
    obtener_socios_con_libros_prestados
)

socios_bp = Blueprint("socios", __name__, url_prefix="/socios")

# ────────────── CREAR SOCIO ──────────────
@socios_bp.route("/crear", methods=["GET", "POST"])
@login_required
def crear_socio_vista():
    form = SocioForm()
    if form.validate_on_submit():
        crear_socio(nombre=form.nombre.data, email=form.email.data)
        flash("Socio creado correctamente", "success")
        return redirect(url_for("socios.listar_socios"))
    return render_template("paginas/socios/socio_crear.html", form=form)

# ────────────── LISTAR SOCIOS ──────────────
@socios_bp.route("/")
@login_required  # opcional: quítalo si quieres que sea público
def listar_socios():
    socios = obtener_todos_los_socios()
    return render_template("paginas/socios/socios_listado.html", socios=socios)

# ────────────── SOCIOS CON LIBROS PRESTADOS ──────────────
@socios_bp.route("/prestamos")
@login_required
def prestamos():
    libros_prestados = obtener_socios_con_libros_prestados()
    return render_template("paginas/socios/socios_prestamos.html", libros=libros_prestados)
