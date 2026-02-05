from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from myapp.forms.libro_form import LibroForm
from myapp.models import libro
from myapp.models.libro import Libro
from myapp.services import libro_service
from myapp.services.libro_service import crear_libro, editar_libro, listar_libros

navigation_bp = Blueprint(
    "navigation",
    __name__,
    url_prefix="/"
)

@navigation_bp.route("/")
def inicio():
    return render_template("paginas/inicio.html")

