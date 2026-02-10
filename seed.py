# seed.py
from myapp import create_app, db
from myapp.models.libro import Libro
from myapp.models.socio import Socio
from myapp.models.user import Usuario


app = create_app()

with app.app_context():
    # ────────────── BORRAR DATOS ANTIGUOS ──────────────
    db.drop_all()
    db.create_all()

    # ────────────── LIBROS ──────────────
    libros = [
        Libro(titulo="El Quijote", autor="Cervantes", resumen="Aventura de Don Quijote", socio_id=1),
        Libro(titulo="1984", autor="George Orwell", resumen="Distopía sobre totalitarismo", socio_id=2),
        Libro(titulo="Cien Años de Soledad", autor="Gabriel García Márquez", resumen="Saga familiar en Macondo", socio_id=None),
        Libro(titulo="El Principito", autor="Antoine de Saint-Exupéry", resumen="Historia poética sobre la infancia", socio_id=None),
        Libro(titulo="La Odisea", autor="Homero", resumen="Viaje de Ulises", socio_id=None),
        Libro(titulo="Don Juan Tenorio", autor="José Zorrilla", resumen="Drama romántico", socio_id=None),
        Libro(titulo="Orgullo y Prejuicio", autor="Jane Austen", resumen="Novela sobre sociedad inglesa", socio_id=None),
        Libro(titulo="Drácula", autor="Bram Stoker", resumen="Novela de terror gótico", socio_id=None),
        Libro(titulo="Frankenstein", autor="Mary Shelley", resumen="Historia del monstruo de Frankenstein", socio_id=None),
        Libro(titulo="El Hobbit", autor="J.R.R. Tolkien", resumen="Aventura de Bilbo Bolsón", socio_id=None)
    ]

    db.session.add_all(libros)

    # ────────────── SOCIOS ──────────────
    socios = [
    Socio(nombre="Juan Pérez", email="juan@example.com"),
    Socio(nombre="María López", email="maria@example.com"),
    Socio(nombre="Carlos García", email="carlos@example.com"),
    Socio(nombre="Ana Torres", email="ana@example.com"),
    Socio(nombre="Luis Fernández", email="luis@example.com"),
    Socio(nombre="Sofía Martínez", email="sofia@example.com"),
    Socio(nombre="Diego Ramírez", email="diego@example.com"),
    Socio(nombre="Elena Gómez", email="elena@example.com"),
    Socio(nombre="Miguel Sánchez", email="miguel@example.com"),
    Socio(nombre="Laura Díaz", email="laura@example.com")
]

    db.session.add_all(socios)

    # ────────────── USUARIOS ──────────────
    admin = Usuario(
        username="admin",
        is_admin=True
    )
    admin.set_password("admin123")
    user1 = Usuario(
        username="user1",
        is_admin=False
    )
    user1.set_password("user123")

    user2 = Usuario(
        username="user2",
        is_admin=False
    )
    user2.set_password("user123")

    db.session.add_all([admin, user1, user2])

    # ────────────── GUARDAR TODO ──────────────
    db.session.commit()
    print("Datos de prueba insertados correctamente")
