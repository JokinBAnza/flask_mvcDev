from sqlalchemy import func
from myapp import db
from myapp.models.libro import Libro
from myapp.models.socio import Socio

# ────────────── LISTAR ──────────────
def listar_libros():
    return Libro.query.all()
    # return Libro.query.order_by(func.lower(Libro.titulo)).all()

def obtener_libro(libro_id):
    return Libro.query.get(libro_id)

# ────────────── CREAR / EDITAR ──────────────
def crear_libro(titulo, autor, resumen=None):
    libro = Libro(titulo=titulo, autor=autor, resumen=resumen)
    db.session.add(libro)
    db.session.commit()
    return libro

def editar_libro(libro_id, titulo=None, autor=None, resumen=None):
    libro = Libro.query.get(libro_id)
    if not libro:
        return None
    if titulo is not None:
        libro.titulo = titulo
    if autor is not None:
        libro.autor = autor
    if resumen is not None:
        libro.resumen = resumen
    db.session.commit()
    return libro

# ────────────── PRESTAR / DEVOLVER ──────────────
def prestar_libro(libro_id, socio_id):
    libro = Libro.query.get(libro_id)
    socio = Socio.query.get(socio_id)
    if not libro or not socio:
        return None
    libro.socio = socio  # correcto
    db.session.commit()
    return libro

def devolver_libro(socio_id):
    socio = Socio.query.get(socio_id)
    if socio and socio.libros:  # usar 'libros', plural
        libro = socio.libros[0]  # obtener el primer libro prestado
        libro.socio = None        # desvincular del socio
        db.session.commit()
        return True
    return False

# ────────────── LISTAR SOCIOS CON PRESTAMOS ──────────────
def listar_socios_con_prestamos():
    return Socio.query.filter(Socio.libros.any()).all()  # any() porque es relación uno a muchos


# ────────────── BÚSQUEDAS ──────────────
def buscar_libros_por_titulo(palabra):
    return Libro.query.filter(Libro.titulo.ilike(f"%{palabra}%")).all()

def listar_libros_disponibles():
    return Libro.query.filter(Libro.socio == None).all()

def listar_socios_con_prestamos():
    return Socio.query.filter(Socio.libro != None).all()
