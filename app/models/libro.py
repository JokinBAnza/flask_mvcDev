from app import db

class Libro(db.Model):
    __tablename__ = "libros"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)  
    autor = db.Column(db.String(100), nullable=False)
    resumen = db.Column(db.Text, nullable=True)
    
    # Relación con Socio para préstamos
    socio_id = db.Column(db.Integer, db.ForeignKey('socio.id'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "resumen": self.resumen,
            "socio_id": self.socio_id
        }
    
    def __repr__(self):
        return f"<Libro {self.titulo} - {self.autor}>"
