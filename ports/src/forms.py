from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
import sqlalchemy as sa
from src import db
from src.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign-in')

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
            User.username == email.data
        ))
        if user is not None:
            raise ValidationError("This email is already in use!")