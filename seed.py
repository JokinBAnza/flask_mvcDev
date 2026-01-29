# seed.py
from myapp import create_app, db
from myapp.models.libro import Libro
from myapp.models.socio import Socio
from myapp.models.prestamo import Prestamo
from myapp.models.user import Usuario
from myapp.services.hashPassword import hash_password  # <- usamos el servicio

app = create_app()

with app.app_context():
    # ────────────── BORRAR DATOS ANTIGUOS ──────────────
    db.drop_all()
    db.create_all()

    # ────────────── LIBROS ──────────────
    libros = [
        Libro(titulo="El Quijote", autor="Cervantes", resumen="Aventura de Don Quijote"),
        Libro(titulo="1984", autor="George Orwell", resumen="Distopía sobre totalitarismo"),
        Libro(titulo="Cien Años de Soledad", autor="Gabriel García Márquez", resumen="Saga familiar en Macondo"),
        Libro(titulo="El Principito", autor="Antoine de Saint-Exupéry", resumen="Historia poética sobre la infancia"),
        Libro(titulo="La Odisea", autor="Homero", resumen="Viaje de Ulises"),
        Libro(titulo="Don Juan Tenorio", autor="José Zorrilla", resumen="Drama romántico"),
        Libro(titulo="Orgullo y Prejuicio", autor="Jane Austen", resumen="Novela sobre sociedad inglesa"),
        Libro(titulo="Drácula", autor="Bram Stoker", resumen="Novela de terror gótico"),
        Libro(titulo="Frankenstein", autor="Mary Shelley", resumen="Historia del monstruo de Frankenstein"),
        Libro(titulo="El Hobbit", autor="J.R.R. Tolkien", resumen="Aventura de Bilbo Bolsón")
    ]
    db.session.add_all(libros)

    # ────────────── SOCIOS ──────────────
    socios = [
        Socio(nombre="Juan Pérez", email="juan@example.com"),
        Socio(nombre="María López", email="maria@example.com"),
        Socio(nombre="Carlos García", email="carlos@example.com"),
        Socio(nombre="Ana Torres", email="ana@example.com"),
        Socio(nombre="Luis Fernández", email="luis@example.com")
    ]
    db.session.add_all(socios)

    # ────────────── USUARIOS ──────────────
    admin = Usuario(
        username="admin",
        password=hash_password("admin123"),  # <- usamos el servicio
        is_admin=True
    )
    user1 = Usuario(
        username="user1",
        password=hash_password("user123"),  # <- usamos el servicio
        is_admin=False
    )
    user2 = Usuario(
        username="user2",
        password=hash_password("user123"),  # <- usamos el servicio
        is_admin=False
    )
    db.session.add_all([admin, user1, user2])

    # ────────────── PRÉSTAMOS DE EJEMPLO ──────────────
    prestamo1 = Prestamo(libro_id=1, socio_id=1)  # El Quijote prestado a Juan
    prestamo2 = Prestamo(libro_id=2, socio_id=2)  # 1984 prestado a María
    db.session.add_all([prestamo1, prestamo2])

    # ────────────── GUARDAR TODO ──────────────
    db.session.commit()
    print("Datos de prueba insertados correctamente")
