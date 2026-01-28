from myapp import db

class Socio(db.Model):
    __tablename__ = "socio"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Socio {self.nombre} - {self.email}>"
