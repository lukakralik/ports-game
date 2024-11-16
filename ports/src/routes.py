from src import app, db
from src.forms import LoginForm
from src.models import User
import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Luka'}

    posts = [
        {
            'author': {'username': 'Hynek'},
            'body': 'Kupuju zlato!'
        },
        {
            'author': {'username': 'David'},
            'body': 'Otroci jsou meta!'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign-in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# view function mapped onto urls / and /index