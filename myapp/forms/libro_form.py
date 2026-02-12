from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class LibroForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[DataRequired(message="El título es obligatorio"), Length(max=200)],
        render_kw={"class": "form-control", "placeholder": "Escribe el título del libro"}
    )

    autor = StringField(
        "Autor",
        validators=[DataRequired(), Length(max=100)],
        render_kw={"class": "form-control", "placeholder": "Escribe el autor"}
    )

    resumen = TextAreaField(
        "Resumen",
        validators=[Length(min=5, max=1000)],
        render_kw={"class": "form-control", "placeholder": "Resumen del libro", "rows": 6}
    )

    genero = StringField(
        "Género",
        validators=[DataRequired(), Length(max=100)],
        render_kw={"class": "form-control", "placeholder": "Escribe el género del libro"}
    )

    anio_publicacion = IntegerField(
        "Año de publicación",
        validators=[DataRequired(), NumberRange(min=-5000, max=2100)],
        render_kw={"class": "form-control", "placeholder": "Escribe el año de publicación"}
    )

    submit = SubmitField("Guardar", render_kw={"class": "btn btn-primary"})
