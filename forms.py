from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, URLField, TextAreaField
from wtforms.validators import Optional, URL, NumberRange, InputRequired, Length


class AddPetForm(FlaskForm):
    name = StringField("Pet Name", validators=[InputRequired()],)
    species = StringField("Species")
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField("Comments", validators=[Optional(), Length(min=10)])


class EditPetForm(FlaskForm):
    name = StringField("Pet Name", validators=[InputRequired()])
    species = StringField("Species", validators=[InputRequired()])
    age = IntegerField("Age", validators=[NumberRange(min=0, max=30), Optional()])
    photo_url = URLField("Photo URL", validators=[URL(), Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])
    available = BooleanField("Available?", validators=[Optional()])