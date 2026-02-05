# myapp/controllers/api_controller.py
from flask import Blueprint, jsonify
from myapp.services.libro_service import (
    listar_libros, listar_libros_disponibles
)

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)

# ────────────── TODOS LOS LIBROS ──────────────
@api_bp.route("/libros", methods=["GET"])
def api_listar_libros():
    libros = listar_libros()
    return jsonify([l.to_dict() for l in libros])

# ────────────── LIBROS DISPONIBLES ──────────────
@api_bp.route("/libros/disponibles", methods=["GET"])
def api_libros_disponibles():
    libros = listar_libros_disponibles()
    return jsonify([l.to_dict() for l in libros])

# ────────────── BUSCAR LIBROS POR TÍTULO ──────────────
@api_bp.route("/libros/buscar/<string:titulo>", methods=["GET"])
def api_buscar_libros(titulo):
    from myapp.services.libro_service import buscar_libros_por_titulo
    libros = buscar_libros_por_titulo(titulo)
    return jsonify([l.to_dict() for l in libros])

# ────────────── SOCIOS CON LIBROS PRESTADOS ──────────────
@api_bp.route("/libros/socios/prestamos", methods=["GET"])
def api_socios_con_prestamos():
    libros = listar_libros()
    resultado = []
    for libro in libros:
        if libro.socio:
            resultado.append({
                "socio_id": libro.socio.id,
                "socio_nombre": libro.socio.nombre,
                "libro_id": libro.id,
                "libro_titulo": libro.titulo
            })
    return jsonify(resultado)
