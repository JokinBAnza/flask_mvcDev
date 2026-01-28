# myapp/controllers/api_controller.py
from flask import Blueprint, jsonify
from myapp.models.libro import Libro
from myapp.models.socio import Socio
from myapp.models.prestamo import Prestamo
from myapp import db

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)

# ────────────── TODOS LOS LIBROS ──────────────
@api_bp.route("/libros", methods=["GET"])
def api_listar_libros():
    libros = Libro.query.all()
    return jsonify([l.to_dict() for l in libros])

# ────────────── LIBROS DISPONIBLES ──────────────
@api_bp.route("/libros/disponibles", methods=["GET"])
def api_libros_disponibles():
    libros = Libro.query.filter_by(prestado=False).all()
    return jsonify([l.to_dict() for l in libros])

# ────────────── BUSCAR LIBROS POR TÍTULO ──────────────
@api_bp.route("/libros/buscar/<string:titulo>", methods=["GET"])
def api_buscar_libros(titulo):
    libros = Libro.query.filter(Libro.titulo.ilike(f"%{titulo}%")).all()
    return jsonify([l.to_dict() for l in libros])

# ────────────── SOCIOS CON LIBROS PRESTADOS ──────────────
@api_bp.route("/libros/socios/prestamos", methods=["GET"])
def api_socios_con_prestamos():
    prestamos_activos = Prestamo.query.filter_by(fecha_devolucion=None).all()
    resultado = []
    for p in prestamos_activos:
        libro = Libro.query.get(p.libro_id)
        socio = Socio.query.get(p.socio_id)
        if libro and socio:
            resultado.append({
                "socio_id": socio.id,
                "socio_nombre": socio.nombre,
                "libro_id": libro.id,
                "libro_titulo": libro.titulo
            })
    return jsonify(resultado)
