from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class LibroForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[DataRequired(message="El título es obligatorio"), Length(max=200)]
    )

    autor = StringField(
        "Autor",
        validators=[DataRequired(), Length(max=100)]
    )

    resumen = TextAreaField(
        "Resumen",
       # validators=[Length(min=5, max=1000)]
    )

    submit = SubmitField("Guardar")

# Formulario para préstamo de libro
class PrestamoForm(FlaskForm):
    libro_id = IntegerField("ID del libro", validators=[DataRequired()])
    socio_id = IntegerField("ID del socio", validators=[DataRequired()])
    submit = SubmitField("Prestar libro")

# Formulario para devolución de libro
class DevolucionForm(FlaskForm):
    socio_id = IntegerField("ID del socio", validators=[DataRequired()])
    submit = SubmitField("Devolver libro")