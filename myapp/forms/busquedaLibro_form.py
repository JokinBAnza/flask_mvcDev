# myapp/forms/busqueda_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class BusquedaLibroForm(FlaskForm):
    q = StringField("Buscar libro", validators=[DataRequired()], render_kw={"placeholder": "Título del libro"})
    submit = SubmitField("Buscar")
