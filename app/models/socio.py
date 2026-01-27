from . import db

class Socio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    libro = db.relationship('Libro', backref='socio', uselist=False)

    def __repr__(self):
        return f"<Socio {self.nombre} - {self.email}>"