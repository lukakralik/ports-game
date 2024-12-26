import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from src import db
from src.models import User

class NewPortForm(FlaskForm):
    port_name = StringField("Port name", validators=[DataRequired()])
    pirate_port = BooleanField("Pirate port", validators=[DataRequired()])
    rice = IntegerField("Rice", validators=[DataRequired()])
    tea = IntegerField("Tea", validators=[DataRequired()])
    wine = IntegerField("Wine", validators=[DataRequired()])
    spice = IntegerField("Spice", validators=[DataRequired()])
    gold = IntegerField("Gold", validators=[DataRequired()])
    diamonds = IntegerField("Diamonds", validators=[DataRequired()])
    slaves = IntegerField("Slaves", validators=[DataRequired()])
    port_register = SubmitField("Initialize a port")
class NewCrewForm(FlaskForm):
    crew_name = StringField("Port name", validators=[DataRequired()])
    crew_register = SubmitField("Initialize a port")

class RegistrationForm(FlaskForm):
    #username
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password once again', validators=[DataRequired(), EqualTo("password1")])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign-in')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data
        ))
        if user is not None:
            raise ValidationError("This username is already taken!")

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data
        ))
        if user is not None:
            raise ValidationError("This email is already in use!")

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username


    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data
            ))

            if user is not None:
                raise ValidationError("This username is already in use!")