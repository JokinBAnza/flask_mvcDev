from myapp import db
from sqlalchemy import Boolean  # necesario para el tipo Boolean

class Libro(db.Model):
    __tablename__ = "libros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    resumen = db.Column(db.Text, nullable=True)

    # Relación con socio
    socio_id = db.Column(db.Integer, db.ForeignKey("socio.id"), nullable=True)
    socio = db.relationship("Socio", backref="libros")

    # Nueva columna para saber si el libro está prestado
    prestado = db.Column(Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "resumen": self.resumen,
            "socio_id": self.socio_id,
            "prestado": self.prestado  # <-- ahora solo devuelve el valor
        }

    def __repr__(self):
        return f"<Libro {self.titulo} - {self.autor}>"
