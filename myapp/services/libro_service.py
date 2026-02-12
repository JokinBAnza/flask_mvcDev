# myapp/services/libro_service.py
from myapp import db
from myapp.models.libro import Libro
from myapp.models.socio import Socio

# ────────────── LISTAR ──────────────
def listar_libros() -> list[Libro]:
    """Devuelve todos los libros."""
    return Libro.query.all()

def obtener_libro(libro_id: int) -> Libro | None:
    """Devuelve un libro por su ID."""
    return Libro.query.get(libro_id)

# ────────────── CREAR / EDITAR ──────────────
def crear_libro(titulo: str, autor: str, resumen: str | None = None,
                genero: str | None = None, anio_publicacion: int | None = None,
                socio_id: int | None = None) -> Libro:
    """Crea un libro y lo guarda en la base de datos."""
    libro = Libro(
        titulo=titulo,
        autor=autor,
        resumen=resumen,
        genero=genero,
        anio_publicacion=anio_publicacion,
        socio_id=socio_id
    )
    db.session.add(libro)
    db.session.commit()
    return libro

def editar_libro(libro_id: int, titulo: str | None = None,
                 autor: str | None = None, resumen: str | None = None,
                 genero: str | None = None, anio_publicacion: int | None = None) -> Libro | None:
    """Edita un libro existente."""
    libro = Libro.query.get(libro_id)
    if not libro:
        return None
    if titulo is not None:
        libro.titulo = titulo
    if autor is not None:
        libro.autor = autor
    if resumen is not None:
        libro.resumen = resumen
    if genero is not None:
        libro.genero = genero
    if anio_publicacion is not None:
        libro.anio_publicacion = anio_publicacion
    db.session.commit()
    return libro

# ────────────── PRESTAR / DEVOLVER ──────────────
def prestar_libro(libro_id: int, socio_id: int) -> Libro | None:
    """Asocia un libro a un socio (prestado)."""
    libro = Libro.query.get(libro_id)
    socio = Socio.query.get(socio_id)
    if not libro or not socio:
        return None
    libro.socio = socio
    db.session.commit()
    return libro

def devolver_libro(libro_id: int) -> bool:
    """Marca un libro como devuelto (desvincula socio)."""
    libro = Libro.query.get(libro_id)
    if libro and libro.socio is not None:
        libro.socio = None
        db.session.commit()
        return True
    return False

# ────────────── BÚSQUEDAS ──────────────
def buscar_libros_por_titulo(palabra: str) -> list[Libro]:
    """Busca libros por título (insensible a mayúsculas)."""
    return Libro.query.filter(Libro.titulo.ilike(f"%{palabra}%")).all()

# ────────────── LISTAR SOCIOS ──────────────
def listar_socios_con_prestamos() -> list[Socio]:
    """Devuelve todos los socios que tienen al menos un libro prestado."""
    return Socio.query.filter(Socio.libros.any()).all()

def listar_socios_disponibles() -> list[Socio]:
    """Devuelve todos los socios que no tienen ningún libro prestado."""
    return Socio.query.filter(~Socio.libros.any()).all()

# ────────────── LISTAR LIBROS DISPONIBLES ──────────────
def listar_libros_disponibles() -> list[Libro]:
    """Devuelve todos los libros que no están prestados."""
    return Libro.query.filter(Libro.socio == None).all()

# ────────────── BORRAR LIBROS NO PRESTADOS ──────────────
def borrar_libro(libro_id: int) -> bool:
    """Borra un libro si no está prestado. Devuelve True si se borró, False si estaba prestado o no existe."""
    libro = Libro.query.get(libro_id)
    if libro and libro.socio is None:
        db.session.delete(libro)
        db.session.commit()
        return True
    return False
