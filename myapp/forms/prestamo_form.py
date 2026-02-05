from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

# Formulario para préstamo de libro
class PrestamoForm(FlaskForm):
    libro_id = SelectField("Libro", coerce=int, validators=[DataRequired()])
    socio_id = SelectField("Socio", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Prestar libro")