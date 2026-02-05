# myapp/services/socio_service.py
from myapp import db
from myapp.models.socio import Socio
from myapp.models.libro import Libro

def crear_socio(nombre: str, email: str) -> Socio:
    """Crea un socio y lo guarda en la base de datos."""
    socio = Socio(nombre=nombre, email=email)
    db.session.add(socio)
    db.session.commit()
    return socio

def obtener_todos_los_socios() -> list[Socio]:
    """Devuelve todos los socios."""
    return Socio.query.all()

def obtener_socio_por_id(socio_id: int) -> Socio | None:
    """Devuelve un socio por su ID, o None si no existe."""
    return Socio.query.get(socio_id)

def obtener_socios_con_libros_prestados() -> list[tuple[Libro, Socio]]:
    """
    Devuelve una lista de tuplas (libro, socio) con los libros que están prestados.
    Asume que un libro está prestado si `libro.socio_id` no es None.
    """
    libros_prestados = Libro.query.filter(Libro.socio_id.isnot(None)).all()
    return [(libro, libro.socio) for libro in libros_prestados]


def obtener_socio(socio_id: int) -> Socio | None:
    return Socio.query.get(socio_id)

def editar_socio(socio_id: int, nombre: str, email: str) -> Socio | None:
    socio = Socio.query.get(socio_id)
    if not socio:
        return None
    socio.nombre = nombre
    socio.email = email
    db.session.commit()
    return socio

def tiene_libros_prestados(socio_id: int) -> bool:
    """Devuelve True si el socio tiene libros prestados."""
    return Libro.query.filter_by(socio_id=socio_id).count() > 0

def borrar_socio(socio_id: int) -> bool:
    """Borra un socio si no tiene libros prestados. Devuelve True si se borró, False si no existe o tiene libros."""
    socio = Socio.query.get(socio_id)
    if not socio:
        return False
    if tiene_libros_prestados(socio_id):
        return False
    db.session.delete(socio)
    db.session.commit()
    return True