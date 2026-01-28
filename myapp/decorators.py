from functools import wraps
from flask import flash, redirect, url_for
from myapp.models.libro import Libro
from myapp.models.socio import Socio
from flask_login import current_user, login_required

def libro_disponible(f):
    @wraps(f)
    def wrapper(libro_id, socio_id, *args, **kwargs):
        libro = Libro.query.get(libro_id)
        socio = Socio.query.get(socio_id)
        if not libro:
            flash('El libro no existe', 'danger')
            return redirect(url_for('libros.listar'))
        if not socio:
            flash('El socio no existe', 'danger')
            return redirect(url_for('libros.listar'))
        if libro.socio:
            flash('El libro ya está prestado', 'danger')
            return redirect(url_for('libros.listar'))
        if socio.libros:
            flash('El socio ya tiene un libro', 'danger')
            return redirect(url_for('libros.listar'))
        return f(libro_id, socio_id, *args, **kwargs)
    return wrapper

def role_required(role="admin"):
    def decorator(f):
        @wraps(f)
        @login_required
        def wrapper(*args, **kwargs):
            if role == "admin" and not getattr(current_user, "is_admin", False):
                flash("No tienes permisos para acceder a esta página", "danger")
                return redirect(url_for("navigation.inicio"))
            return f(*args, **kwargs)
        return wrapper
    return decorator
