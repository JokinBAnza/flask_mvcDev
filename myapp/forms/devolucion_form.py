from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

# Formulario para devolución de libro
class DevolucionForm(FlaskForm):
    socio_id = SelectField("Socio", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Devolver libro")
