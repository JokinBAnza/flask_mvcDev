from myapp import db

class Prestamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libros.id'))
    socio_id = db.Column(db.Integer, db.ForeignKey('socio.id'))
    fecha_devolucion = db.Column(db.Date, nullable=True)
