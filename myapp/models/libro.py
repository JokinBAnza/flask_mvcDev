from myapp import db

class Libro(db.Model):
    __tablename__ = "libros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    resumen = db.Column(db.Text, nullable=True)

    genero = db.Column(db.String(100), nullable=False)
    anio_publicacion = db.Column(db.Integer, nullable=False)

    # Relación con socio
    socio_id = db.Column(db.Integer, db.ForeignKey("socio.id"), nullable=True)
    socio = db.relationship("Socio", backref="libros")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "resumen": self.resumen,
            "genero": self.genero,
            "anio_publicacion": self.anio_publicacion,
            "socio_id": self.socio_id,
        }

    def __repr__(self):
        return f"<Libro {self.titulo} - {self.autor}>"
