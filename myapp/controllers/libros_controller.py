from flask import Blueprint, request, render_template, redirect, url_for, flash
from myapp.models.libro import Libro
from flask_login import login_required
from myapp.models.socio import Socio
from myapp import db
from myapp.models.prestamo import Prestamo
from myapp.services.libros_service import (
    listar_libros, crear_libro, editar_libro,
    prestar_libro, devolver_libro, buscar_libros_por_titulo
)
from myapp.forms.libro_form import LibroForm, PrestamoForm, DevolucionForm
from myapp.decorators import libro_disponible, role_required

libros_bp = Blueprint(
    "libros",
    __name__,
    url_prefix="/libros"
)

# ────────────── LISTAR ─────────────
@libros_bp.route("/")
def listar():
    libros = Libro.query.all()
    libros_estado = []

    for libro in libros:
        # Buscar préstamo activo para este libro
        prestamo_activo = Prestamo.query.filter_by(libro_id=libro.id, fecha_devolucion=None).first()
        estado = "Prestado" if prestamo_activo else "Disponible"
        libros_estado.append((libro, estado))

    return render_template("paginas/libros/libros.html", libros=libros_estado)


@libros_bp.route("/grid")
def grid():
    libros = listar_libros()
    return render_template("paginas/libros/librosGrid.html", libros=libros)

# ────────────── DETALLE Y EDICIÓN ──────────────
@libros_bp.route("/<int:id>", methods=["GET", "POST"])
@login_required
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
@login_required
@role_required("admin")
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
@login_required
@role_required("admin")
def prestar():
    form = PrestamoForm()

    # --- Libros disponibles: solo los que no tienen préstamo activo ---
    libros_prestados = db.session.query(Prestamo.libro_id).filter(Prestamo.fecha_devolucion == None)
    libros_disponibles = Libro.query.filter(~Libro.id.in_(libros_prestados)).all()
    form.libro_id.choices = [(0, "Seleccione un libro")] + [(l.id, l.titulo) for l in libros_disponibles]

    # --- Socios disponibles: solo los que no tienen préstamo activo ---
    socios_con_prestamo = db.session.query(Prestamo.socio_id).filter(Prestamo.fecha_devolucion == None)
    socios_disponibles = Socio.query.filter(~Socio.id.in_(socios_con_prestamo)).all()
    form.socio_id.choices = [(0, "Seleccione un socio")] + [(s.id, s.nombre) for s in socios_disponibles]

    # --- Validación formulario ---
    if form.validate_on_submit():
        if form.libro_id.data == 0 or form.socio_id.data == 0:
            flash("Debes seleccionar un libro y un socio", "danger")
        else:
            # Crear el préstamo
            prestamo = Prestamo(
                libro_id=form.libro_id.data,
                socio_id=form.socio_id.data
            )
            db.session.add(prestamo)

            # Opcional: marcar libro como prestado
            libro = Libro.query.get(form.libro_id.data)
            libro.prestado = True

            db.session.commit()

            flash("Libro prestado correctamente", "success")
            return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_prestamo.html", form=form)


@libro_disponible
def _prestar_libro(libro_id, socio_id):
    prestar_libro(libro_id, socio_id)
    flash("Libro prestado correctamente", "success")
    return redirect(url_for("libros.listar"))

# ────────────── DEVOLVER ──────────────
@libros_bp.route("/devolver", methods=["GET", "POST"])
@login_required
@role_required("admin")
def devolver():
    form = DevolucionForm()

    # Filtrar socios con préstamo activo
    socios_con_prestamo = db.session.query(Prestamo.socio_id).filter(Prestamo.fecha_devolucion == None)
    socios_disponibles = Socio.query.filter(Socio.id.in_(socios_con_prestamo)).all()
    form.socio_id.choices = [(s.id, s.nombre) for s in socios_disponibles]

    if form.validate_on_submit():
        # Buscar el préstamo activo
        prestamo = Prestamo.query.filter_by(socio_id=form.socio_id.data, fecha_devolucion=None).first()
        if prestamo:
            prestamo.fecha_devolucion = db.func.current_date()
            libro = Libro.query.get(prestamo.libro_id)
            libro.prestado = False
            db.session.commit()
            flash("Libro devuelto correctamente", "success")
        else:
            flash("El socio no tiene ningún libro prestado", "danger")

        return redirect(url_for("libros.listar"))

    return render_template("paginas/libros/libro_devolver.html", form=form)


# ────────────── LIBROS PRESTADOS ──────────────
@libros_bp.route("/prestados")
@login_required
def libros_prestados():
    prestamos_activos = Prestamo.query.filter_by(fecha_devolucion=None).all()
    libros = [(Libro.query.get(p.libro_id), Socio.query.get(p.socio_id)) for p in prestamos_activos]
    return render_template("paginas/libros/libros_prestados.html", libros=libros)



# ────────────── BUSCAR ──────────────
@libros_bp.route("/buscar", methods=["GET"])
def buscar():
    palabra = request.args.get("q", "")
    libros = buscar_libros_por_titulo(palabra)
    return render_template("paginas/libros/libros.html", libros=libros, busqueda=palabra)
