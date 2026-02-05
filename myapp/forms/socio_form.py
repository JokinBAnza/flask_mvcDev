from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class SocioForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email("El formato no es correcto")])  # ⚠ obligatorio
    submit = SubmitField("Guardar")
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class SocioForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Guardar")