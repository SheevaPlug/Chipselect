from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length

class SearchForm(FlaskForm):
    query = StringField('Suche', validators=[
        InputRequired(message='Dieses Feld benötigt eine Eingabe.'),
        Length(min=3, message='Die Eingabe muß mindestens drei Zeichen enthalten.')])
