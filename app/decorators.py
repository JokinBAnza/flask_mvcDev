from functools import wraps
from flask import flash, redirect, url_for
from app.models.libro import Libro
from app.models.socio import Socio

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
        if socio.libro:
            flash('El socio ya tiene un libro', 'danger')
            return redirect(url_for('libros.listar'))
        return f(libro_id, socio_id, *args, **kwargs)
    return wrapper
