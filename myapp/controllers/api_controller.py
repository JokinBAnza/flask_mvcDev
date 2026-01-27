from flask import Blueprint, jsonify, request
from myapp.services.libros_service import listar_libros
api_bp = Blueprint(
    "api",
    __name__,       
    url_prefix="/api"
)

@api_bp.route("/listar", methods=["GET"])
def listar():
    libros = listar_libros()
    return jsonify([l.to_dict() for l in libros])   