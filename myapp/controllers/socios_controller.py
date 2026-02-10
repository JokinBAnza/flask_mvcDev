# myapp/controllers/socios_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from myapp.decorators import role_required
from myapp.forms.socio_form import SocioForm
from myapp.services.socio_service import (
    borrar_socio,
    crear_socio,
    obtener_todos_los_socios,
    obtener_socios_con_libros_prestados,
    tiene_libros_prestados
)

socios_bp = Blueprint("socios", __name__, url_prefix="/socios")

# ────────────── CREAR SOCIO ──────────────
@socios_bp.route("/crear", methods=["GET", "POST"])
@login_required
@role_required("admin")
def crear_socio_vista():
    form = SocioForm()
    if form.validate_on_submit():
        crear_socio(nombre=form.nombre.data, email=form.email.data)
        flash("Socio creado correctamente", "success")
        return redirect(url_for("socios.listar_socios"))
    return render_template("paginas/socios/socio_crear.html", form=form)

# ────────────── LISTAR SOCIOS ──────────────
@socios_bp.route("/")
@login_required
def listar_socios():
    from myapp.services.socio_service import obtener_todos_los_socios, tiene_libros_prestados
    from flask import request

    q = request.args.get("q", "").strip()         # búsqueda por nombre/email
    prestamo = request.args.get("prestamo")       # checkbox: si existe, filtrar socios con libro prestado

    socios = obtener_todos_los_socios()

    # Filtrar por búsqueda
    if q:
        socios = [
            s for s in socios
            if q.lower() in s.nombre.lower() or q.lower() in s.email.lower()
        ]

    # Filtrar solo socios con libro prestado
    if prestamo:
        socios = [s for s in socios if tiene_libros_prestados(s.id)]

    return render_template("paginas/socios/socios_listado.html", socios=socios)

# ────────────── SOCIOS CON LIBROS PRESTADOS ──────────────
@socios_bp.route("/prestamos")
@login_required
@role_required("admin")
def prestamos():
    libros_prestados = obtener_socios_con_libros_prestados()
    return render_template("paginas/socios/socios_prestamos.html", libros=libros_prestados)

# ────────────── EDITAR SOCIO ──────────────
@socios_bp.route("/editar/<int:socio_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def editar_socio_vista(socio_id):
    from myapp.services.socio_service import obtener_socio, editar_socio

    socio = obtener_socio(socio_id)
    if not socio:
        flash("Socio no encontrado", "error")
        return redirect(url_for("socios.listar_socios"))

    form = SocioForm(obj=socio)  # rellena el form con los datos actuales

    if form.validate_on_submit():
        editar_socio(socio_id, nombre=form.nombre.data, email=form.email.data)
        flash("Socio actualizado correctamente", "success")
        return redirect(url_for("socios.listar_socios"))

    return render_template("paginas/socios/socio_editar.html", form=form, socio=socio)


# ────────────── BORRAR SOCIO ──────────────
from flask import jsonify, request

@socios_bp.route("/borrar/<int:socio_id>", methods=["POST"])
@login_required
@role_required("admin")
def borrar_socio_vista(socio_id):
    mensaje = ""
    categoria = ""

    if tiene_libros_prestados(socio_id):
        mensaje = "No se puede eliminar el socio porque tiene libros prestados."
        categoria = "error"
    elif borrar_socio(socio_id):
        mensaje = "Socio eliminado correctamente."
        categoria = "success"
    else:
        mensaje = "Socio no encontrado."
        categoria = "error"

    # No necesitamos AJAX para el form normal
    flash(mensaje, categoria)
    return redirect(url_for("socios.listar_socios"))

