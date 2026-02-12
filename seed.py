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
    db.session.commit()  # Necesario para que tengan ID

    # ────────────── LIBROS ──────────────
    libros = [
        Libro(titulo="El Quijote", autor="Cervantes",
              resumen="Aventura de Don Quijote",
              genero="Novela", anio_publicacion=1605,
              socio=socios[0]),

        Libro(titulo="1984", autor="George Orwell",
              resumen="Distopía sobre totalitarismo",
              genero="Ciencia ficción", anio_publicacion=1949,
              socio=socios[1]),

        Libro(titulo="Cien Años de Soledad",
              autor="Gabriel García Márquez",
              resumen="Saga familiar en Macondo",
              genero="Realismo mágico", anio_publicacion=1967),

        Libro(titulo="El Principito",
              autor="Antoine de Saint-Exupéry",
              resumen="Historia poética sobre la infancia",
              genero="Fábula", anio_publicacion=1943),

        Libro(titulo="La Odisea",
              autor="Homero",
              resumen="Viaje de Ulises",
              genero="Épica", anio_publicacion=-800),

        Libro(titulo="Don Juan Tenorio",
              autor="José Zorrilla",
              resumen="Drama romántico",
              genero="Teatro", anio_publicacion=1844),

        Libro(titulo="Orgullo y Prejuicio",
              autor="Jane Austen",
              resumen="Novela sobre sociedad inglesa",
              genero="Romance", anio_publicacion=1813),

        Libro(titulo="Drácula",
              autor="Bram Stoker",
              resumen="Novela de terror gótico",
              genero="Terror", anio_publicacion=1897),

        Libro(titulo="Frankenstein",
              autor="Mary Shelley",
              resumen="Historia del monstruo de Frankenstein",
              genero="Terror", anio_publicacion=1818),

        Libro(titulo="El Hobbit",
              autor="J.R.R. Tolkien",
              resumen="Aventura de Bilbo Bolsón",
              genero="Fantasía", anio_publicacion=1937)
    ]

    db.session.add_all(libros)

    # ────────────── USUARIOS ──────────────
    admin = Usuario(username="admin", is_admin=True)
    admin.set_password("admin123")

    user1 = Usuario(username="user1", is_admin=False)
    user1.set_password("user123")

    user2 = Usuario(username="user2", is_admin=False)
    user2.set_password("user123")

    db.session.add_all([admin, user1, user2])

    # ────────────── GUARDAR TODO ──────────────
    db.session.commit()
    print("Datos de prueba insertados correctamente")
