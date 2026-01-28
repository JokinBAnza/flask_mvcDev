from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from myapp.forms.socio_form import SocioForm
from myapp.models.socio import Socio
from myapp.models.libro import Libro
from myapp import db
from myapp.models.prestamo import Prestamo

socios_bp = Blueprint("socios", __name__, url_prefix="/socios")

# ────────────── CREAR SOCIO ──────────────
@socios_bp.route("/crear", methods=["GET", "POST"])
@login_required
def crear_socio():
    form = SocioForm()
    if form.validate_on_submit():
        nuevo_socio = Socio(
            nombre=form.nombre.data,
            email=form.email.data
        )
        db.session.add(nuevo_socio)
        db.session.commit()
        flash("Socio creado correctamente", "success")
        return redirect(url_for("socios.listar_socios"))
    return render_template("paginas/socios/socio_crear.html", form=form)

# ────────────── LISTAR SOCIOS ──────────────
@socios_bp.route("/")
@login_required  # opcional: quítalo si quieres que sea público
def listar_socios():
    socios = Socio.query.all()
    return render_template("paginas/socios/socios_listado.html", socios=socios)

# ────────────── SOCIOS CON LIBROS PRESTADOS ──────────────
@socios_bp.route("/prestamos")
@login_required
def prestamos():
    prestamos_activos = Prestamo.query.filter_by(fecha_devolucion=None).all()
    libros_prestados = [(Libro.query.get(p.libro_id), Socio.query.get(p.socio_id)) for p in prestamos_activos]
    return render_template("paginas/socios/socios_prestamos.html", libros=libros_prestados)
