from datetime import datetime, timezone
from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import flash, redirect, render_template, request, url_for

from src import app, db
from src.forms import NewPortForm, NewCrewForm
from src.models import Port, Crew


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')
    

@app.route('/login')
def login():
    ports = Port.query.all()
    
    return render_template('login.html', title='Port login', ports=ports)

# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = db.first_or_404(sa.select(User).where(User.username == username))
#     posts = [
#         {'author': user, 'body': 'Test post #1'},
#         {'author': user, 'body': 'Test post #2'}
#     ]
#     return render_template('user.html', user=user, posts=posts)

# @app.route('/edit_profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm(current_user.username)

#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.about_me = form.about_me.data
#         db.session.commit()
#         flash("Changes have been saved!")
#         return redirect(url_for("edit_profile"))

#     elif request.method == "GET":
#         form.username.data = current_user.username
#         form.about_me.data = current_user.about_me
#     return render_template("edit_profile.html", title="Edit profile", form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template("admin/admin.html", title="Admin")

@app.route('/admin/new_port', methods=['GET', 'POST'])
def new_port():
    form = NewPortForm()
    if form.validate_on_submit():
        port = Port(
            name=form.port_name.data,
            pirate=form.pirate_port.data,
            rice_price=form.rice.data,
            tea_price=form.tea.data,
            wine_price=form.wine.data,
            spice_price=form.spice.data,
            gold_price=form.gold.data,
            diamonds_price=form.diamonds.data,
            slaves_price=form.slaves.data
        )
        db.session.add(port)
        db.session.commit()
        flash('New port has been initialized successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('admin/new_port.html', form=form)

@app.route('/admin/new_crew', methods=['GET', 'POST'])
def new_crew():
    form = NewCrewForm()
    if form.validate_on_submit():
        
        crew = Crew(name=form.crew_name.data, color=form.crew_color.data)
        
        db.session.add(crew)
        db.session.commit()
        
        flash(f'Crew "{form.crew_name.data}" with color "{form.crew_color.data}" registered successfully!', 'success')
        return redirect(url_for('admin'))
    return render_template('admin/new_crew.html', form=form)

@app.route('/port/<int:port_id>')
def port_detail(port_id):
    port = Port.query.get_or_404(port_id)
    crews = Crew.query.all()
    return render_template('port_detail.html', port=port, crews = crews)

@app.route('/port/<int:port_id><int:crew_id>')
def crew_operation(port_id, crew_id):
    port = Port.query.get_or_404(port_id)
    crew = Crew.query.get_or_404(crew_id)
    return render_template('crew_operation.html', port=port, crew=crew)

@app.route('/offers')
def offers():
    return render_template('offers.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

# view function mapped onto urls / and /index