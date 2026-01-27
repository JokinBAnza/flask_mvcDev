from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models.libro import Libro
from app.services.libros_service import (
    listar_libros, crear_libro, editar_libro,
    prestar_libro, devolver_libro, buscar_libros_por_titulo
)
from app.forms.libro_form import LibroForm, PrestamoForm, DevolucionForm
from app.decorators import libro_disponible

libros_bp = Blueprint(
    "libros",
    __name__,
    url_prefix="/libros"
)

# ────────────── LISTAR ──────────────
@libros_bp.route("/")
def listar():
    libros = listar_libros()
    return render_template("paginas/libros/libros.html", libros=libros)

@libros_bp.route("/grid")
def grid():
    libros = listar_libros()
    return render_template("paginas/libros/librosGrid.html", libros=libros)

# ────────────── DETALLE Y EDICIÓN ──────────────
@libros_bp.route("/<int:id>", methods=["GET", "POST"])
def detalle(id):
    libro = Libro.query.get_or_404(id)
    form = LibroForm(obj=libro)
    if form.validate_on_submit():
        editar_libro(
            libro_id=id,
            titulo=form.titulo.data,
            autor=form.autor.data,
            resumen=form.resumen.data
        )
        flash("Libro actualizado correctamente", "success")
        return redirect(url_for("libros.listar"))
    return render_template("paginas/libros/libro_editar.html", form=form, libro=libro)

# ────────────── CREAR ──────────────
@libros_bp.route("/crear", methods=["GET", "POST"])
def crear():
    form = LibroForm()
    if form.validate_on_submit():
        crear_libro(
            titulo=form.titulo.data,
            autor=form.autor.data,
            resumen=form.resumen.data
        )
        flash("Libro creado correctamente", "success")
        return redirect(url_for("libros.listar"))
    return render_template("paginas/libros/libro_crear.html", form=form)

# ────────────── PRESTAR ──────────────
@libros_bp.route("/prestar", methods=["GET", "POST"])
def prestar():
    form = PrestamoForm()
    if form.validate_on_submit():
        return _prestar_libro(form.libro_id.data, form.socio_id.data)
    return render_template("paginas/libros/libro_prestamo.html", form=form)

@libro_disponible
def _prestar_libro(libro_id, socio_id):
    prestar_libro(libro_id, socio_id)
    flash("Libro prestado correctamente", "success")
    return redirect(url_for("libros.listar"))

# ────────────── DEVOLVER ──────────────
@libros_bp.route("/devolver", methods=["GET", "POST"])
def devolver():
    form = DevolucionForm()
    if form.validate_on_submit():
        if devolver_libro(form.socio_id.data):
            flash("Libro devuelto correctamente", "success")
        else:
            flash("El socio no tiene ningún libro prestado", "danger")
        return redirect(url_for("libros.listar"))
    return render_template("paginas/libros/libro_devolver.html", form=form)

# ────────────── BUSCAR ──────────────
@libros_bp.route("/buscar", methods=["GET"])
def buscar():
    palabra = request.args.get("q", "")
    libros = buscar_libros_por_titulo(palabra)
    return render_template("paginas/libros/libros.html", libros=libros, busqueda=palabra)
