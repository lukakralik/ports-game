import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from src import db
from src.models import Port


class NewPortForm(FlaskForm):
    port_name = StringField("Port name", validators=[DataRequired()])
    pirate_port = BooleanField("Pirate port")
    rice = IntegerField("Rice", validators=[DataRequired()])
    tea = IntegerField("Tea", validators=[DataRequired()])
    wine = IntegerField("Wine", validators=[DataRequired()])
    spice = IntegerField("Spice", validators=[DataRequired()])
    gold = IntegerField("Gold", validators=[DataRequired()])
    diamonds = IntegerField("Diamonds", validators=[DataRequired()])
    slaves = IntegerField("Slaves", validators=[DataRequired()])
    port_register = SubmitField("Initialize a port")


class NewCrewForm(FlaskForm):
    crew_name = StringField("Crew Name", validators=[DataRequired()])
    crew_color = SelectField(
        "Crew Color",
        choices=[
            ("red", "Red"),
            ("blue", "Blue"),
            ("green", "Green"),
            ("yellow", "Yellow"),
            ("black", "Black"),
            ("white", "White"),
            ("orange", "Orange"),
            ("purple", "Purple"),
            ("Brown", "Brown"),
        ],
        validators=[DataRequired()],
    )
    crew_register = SubmitField("Register Crew")