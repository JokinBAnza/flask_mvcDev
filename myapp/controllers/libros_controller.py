# myapp/controllers/libro_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from myapp.forms.libro_form import LibroForm
from myapp.forms.devolucion_form import DevolucionForm
from myapp.forms.prestamo_form import PrestamoForm
from myapp.forms.busquedaLibro_form import BusquedaLibroForm
from myapp.decorators import role_required
from myapp.services.libro_service import (
    listar_libros, obtener_libro, crear_libro, editar_libro,
    prestar_libro, devolver_libro, buscar_libros_por_titulo,
    listar_socios_con_prestamos, listar_libros_disponibles, listar_socios_disponibles
)

libros_bp = Blueprint("libros", __name__, url_prefix="/libros")

# ────────────── LISTAR ──────────────
@libros_bp.route("/")
def listar():
    solo_disponibles = request.args.get("disponibles", default=0, type=int)
    if solo_disponibles:
        libros = listar_libros_disponibles()
    else:
        libros = listar_libros()

    # Creamos el formulario con los datos GET para mantener la búsqueda
    form = BusquedaLibroForm(request.args)

    return render_template("paginas/libros/libros.html", libros=libros, form=form)



# ────────────── GRID ──────────────
@libros_bp.route("/grid")
def grid():
    libros = listar_libros()
    return render_template("paginas/libros/librosGrid.html", libros=libros)


# ────────────── DETALLE Y EDICIÓN ──────────────
@libros_bp.route("/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def detalle(id):
    libro = obtener_libro(id)
    if not libro:
        flash("Libro no encontrado", "danger")
        return redirect(url_for("libros.listar"))

    form = LibroForm(obj=libro)
    if form.validate_on_submit():
        editar_libro(
            libro_id=id,
            titulo=form.titulo.data,
            autor=form.autor.data,
            resumen=form.resumen.data,
            genero=form.genero.data,
            anio_publicacion=form.anio_publicacion.data
        )
        flash("Libro actualizado correctamente", "success")
        return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_editar.html", form=form, libro=libro)


# ────────────── CREAR ──────────────
@libros_bp.route("/crear", methods=["GET", "POST"])
@login_required
@role_required("admin")
def crear():
    form = LibroForm()
    if form.validate_on_submit():
        crear_libro(
            titulo=form.titulo.data,
            autor=form.autor.data,
            resumen=form.resumen.data,
            genero=form.genero.data,
            anio_publicacion=form.anio_publicacion.data
        )
        flash("Libro creado correctamente", "success")
        return redirect(url_for("libros.listar"))


    return render_template("paginas/libros/libro_crear.html", form=form)


# ────────────── PRESTAR ──────────────
@libros_bp.route("/prestar", methods=["GET", "POST"])
@login_required
@role_required("admin")
def prestar():
    form = PrestamoForm()

    # Libros y socios disponibles usando service
    form.libro_id.choices = [(0, "Seleccione un libro")] + [
        (l.id, l.titulo) for l in listar_libros_disponibles()
    ]
    form.socio_id.choices = [(0, "Seleccione un socio")] + [
        (s.id, s.nombre) for s in listar_socios_disponibles()
    ]

    if form.validate_on_submit():
        if form.libro_id.data == 0 or form.socio_id.data == 0:
            flash("Debes seleccionar un libro y un socio", "danger")
        else:
            prestar_libro(form.libro_id.data, form.socio_id.data)
            flash("Libro prestado correctamente", "success")
            return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_prestamo.html", form=form)


# ────────────── DEVOLVER ──────────────
@libros_bp.route("/devolver", methods=["GET", "POST"])
@login_required
@role_required("admin")
def devolver():
    form = DevolucionForm()
    socios = listar_socios_con_prestamos()
    form.socio_id.choices = [(s.id, s.nombre) for s in socios]

    if form.validate_on_submit():
        socio_id = form.socio_id.data
        libro = next((l for l in listar_libros() if l.socio and l.socio.id == socio_id), None)
        if libro:
            devolver_libro(libro.id)
            flash("Libro devuelto correctamente", "success")
        else:
            flash("El socio no tiene ningún libro prestado", "danger")
        return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_devolver.html", form=form)


# ────────────── LIBROS PRESTADOS ──────────────
@libros_bp.route("/prestados")
@login_required
@role_required("admin")
def libros_prestados():
    libros = [(l, l.socio) for l in listar_libros() if l.socio]
    return render_template("paginas/libros/libros_prestados.html", libros=libros)

# ────────────── BORRAR LIBROS ──────────────
@libros_bp.route("/borrar/<int:libro_id>", methods=["POST"])
@role_required("admin")
def borrar(libro_id):
    from myapp.services.libro_service import borrar_libro

    exito = borrar_libro(libro_id)
    if not exito:
        flash("No se puede borrar un libro que está prestado o no existe.", "error")
    else:
        flash("Libro borrado correctamente.", "success")
    return redirect(url_for("libros.listar"))



# ────────────── BUSCAR ──────────────
@libros_bp.route("/buscar", methods=["GET"])
def buscar():
    palabra = request.args.get("q", "")
    libros = buscar_libros_por_titulo(palabra)

    # Creamos el formulario con los datos GET para que tenga el valor de búsqueda
    form = BusquedaLibroForm(request.args)

    return render_template("paginas/libros/libros.html", libros=libros, form=form, busqueda=palabra)