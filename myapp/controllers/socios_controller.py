from flask import Blueprint, render_template, redirect, url_for, flash
from myapp.forms.socio_form import SocioForm
from myapp.models.socio import Socio
from myapp.models.libro import Libro
from myapp import db

socios_bp = Blueprint("socios", __name__, url_prefix="/socios")

# ────────────── CREAR SOCIO ──────────────
@socios_bp.route("/crear", methods=["GET", "POST"])
def crear_socio():
    form = SocioForm()
    if form.validate_on_submit():
        nuevo_socio = Socio(
            nombre=form.nombre.data,
            email=form.email.data  # ⚠ aquí es obligatorio
        )
        db.session.add(nuevo_socio)
        db.session.commit()
        flash("Socio creado correctamente", "success")
        return redirect(url_for("socios.listar_socios"))
    return render_template("paginas/socios/socio_crear.html", form=form)


# ────────────── LISTAR SOCIOS ──────────────
@socios_bp.route("/")
def listar_socios():
    socios = Socio.query.all()
    return render_template("paginas/socios/socios_listado.html", socios=socios)

# ────────────── SOCIOS CON LIBROS PRESTADOS ──────────────
@socios_bp.route("/prestamos")
def prestamos():
    libros_prestados = Libro.query.filter(Libro.socio_id.isnot(None)).all()
    return render_template("paginas/socios/socios_prestamos.html", libros=libros_prestados)
