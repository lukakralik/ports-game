from datetime import datetime, timezone
from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from src import app, db
from src.forms import EditProfileForm, NewPortForm, NewCrewForm, RegistrationForm
from src.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
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

    return render_template('index.html', title='Home', posts=posts)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return(redirect(url_for("index")))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash("Congrats you are now registered")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Changes have been saved!")
        return redirect(url_for("edit_profile"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit profile", form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # if form.validate_on_submit():
    #     current_user.username = form.username.data
    #     current_user.about_me = form.about_me.data
    #     db.session.commit()
    #     flash("Changes have been saved!")
    #     return redirect(url_for("edit_profile"))

    # elif request.method == "GET":
    #     form.username.data = current_user.username
    #     form.about_me.data = current_user.about_me
    return render_template("admin/admin.html", title="Admin")

@app.route('/admin/new_port')
def new_port():
    form = NewPortForm()
    return render_template('admin/new_port.html', form=form)

@app.route('/admin/new_crew')
def new_crew():
    return render_template('admin/new_crew.html')

# view function mapped onto urls / and /index