from src import app
from src.forms import LoginForm
from flask import render_template, flash, redirect

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
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for user {}, remember_me={}".format(
            form.username.data, form.remember_me.data
        ))
        return redirect('/index')
    return render_template('login.html', title='Sign-in', form=form)

# view function mapped onto urls / and /index