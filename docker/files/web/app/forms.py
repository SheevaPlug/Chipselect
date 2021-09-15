from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length

class SearchForm(FlaskForm):
    query = StringField('Suche', validators=[
        InputRequired(message='Dieses Feld benötigt eine Eingabe.'),
        Length(min=1, message='Die Eingabe muß mindestens zwei Zeichen enthalten.')])
