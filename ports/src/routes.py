from datetime import datetime, timedelta, timezone

from flask import flash, g, jsonify, redirect, render_template, request, url_for

from src import app, db
from src.forms import NewCrewForm, NewPortForm
from src.models import Crew, GameTimer, Port
from src.utils import *


@app.before_request
def check_game_over():
    g.game_over = False
    timer = GameTimer.query.first()
    if timer and timer.is_active:
        if datetime.now() >= timer.end_time:
            timer.is_active = False
            db.session.commit()
            g.game_over = True
        else:
            g.game_over = False

@app.route('/timer_status')
def timer_status():
    timer = GameTimer.query.first()
    if timer and timer.is_active:
        current_time = datetime.now()
        if current_time >= timer.end_time:
            timer.is_active = False
            db.session.commit()
            return jsonify({'seconds_left': 0, 'is_active': False})
        remaining = timer.end_time - current_time
        seconds_left = int(remaining.total_seconds())
        return jsonify({'seconds_left': seconds_left, 'is_active': True})
    return jsonify({'seconds_left': 0, 'is_active': False})

@app.context_processor
def inject_game_state():
    return dict(game_over=g.get('game_over', False))

@app.route('/admin/start_timer', methods=['POST'])
def start_timer():
    minutes = request.form.get('minutes', type=int)
    if not minutes or minutes < 1:
        flash('Invalid duration', 'danger')
        return redirect(url_for('admin'))
    
    end_time = datetime.now() + timedelta(minutes=minutes)
    timer = GameTimer.query.first()
    if timer:
        timer.end_time = end_time
        timer.is_active = True
    else:
        timer = GameTimer(end_time=end_time, is_active=True)
        db.session.add(timer)
    db.session.commit()
    flash(f'Timer set for {minutes} minutes!', 'success')
    return redirect(url_for('admin'))


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


@app.route("/login")
def login():
    ports = Port.query.all()

    return render_template("login.html", title="Port login", ports=ports)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("admin/admin.html", title="Admin")

@app.route("/manual", methods=["GET", "POST"])
def manual():
    return render_template("manual.html", title="Manual")


@app.route("/admin/new_port", methods=["GET", "POST"])
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
            canon_price=form.canons.data,
        )
        db.session.add(port)
        db.session.commit()
        flash("New port has been initialized successfully.", "success")
        return redirect(url_for("admin"))
    return render_template("admin/new_port.html", form=form)

@app.route("/list_crews", methods=["GET"])
def list_crews():
    crews=Crew.query.all()
    return render_template("admin/list_crews.html", crews=crews)

@app.route("/list_ports", methods=["GET"])
def list_ports():
    ports=Port.query.all()
    return render_template("admin/list_ports.html", ports=ports)

@app.route("/delete_crew<string:crew_name>", methods=["POST"])
def delete_crew(crew_name):
    queried_crew = Crew.query.filter_by(name=crew_name).first()
    crews = Crew.query.all()

    if queried_crew:
        db.session.delete(queried_crew)
        db.session.commit()
        flash("Crew deleted", "success")
        crews = Crew.query.all()
        return render_template("admin/list_crews.html", crews=crews)
    flash("Crew not found", "failure")
    return render_template("admin/list_crews.html", crews=crews)
    
@app.route("/delete_port<string:port_name>", methods=["POST"])
def delete_port(port_name):
    queried_port = Port.query.filter_by(name=port_name).first()
    ports = Crew.query.all()

    if queried_port:
        db.session.delete(queried_port)
        db.session.commit()
        flash("Port deleted", "success")
        ports = Crew.query.all()
        return render_template("admin/list_ports.html", ports=ports)
    flash("Port not found", "failure")
    return render_template("admin/list_ports.html", ports=ports)



@app.route("/new_crew", methods=["GET", "POST"])
def new_crew():
    form = NewCrewForm()
    if form.validate_on_submit():
        crew_color = form.crew_color.data
        taken_colors = [crew.color for crew in Crew.query.all()]
        if crew_color in taken_colors:
            flash(
                f'The color "{crew_color}" is already taken. Taken colors: {", ".join(taken_colors)}',
                "danger",
            )
            return redirect(url_for("new_crew"))

        crew = Crew(
            name=form.crew_name.data,
            color=form.crew_color.data,
            max_carry=3,
            current_carry=0,
            balance=50,
            rice_count=0,
            tea_count=0,
            wine_count=0,
            spice_count=0,
            gold_count=0,
            canon_count=0,
            diamonds_count=0,
            is_pirate=False,
        )
        db.session.add(crew)
        db.session.commit()

        flash("Crew added successfully!", "success")
        return redirect(url_for("admin"))
    return render_template("admin/new_crew.html", form=form)


@app.route("/port/<int:port_id>")
def port_detail(port_id):
    port = Port.query.get_or_404(port_id)
    crews = Crew.query.all()
    return render_template("port_detail.html", port=port, crews=crews)


@app.route("/port/<int:port_id><int:crew_id>")
def crew_operation(port_id, crew_id):
    port = Port.query.get_or_404(port_id)
    crew = Crew.query.get_or_404(crew_id)
    crews = Crew.query.all()
    return render_template("crew_operation.html", port=port, crew=crew, crews=crews)


@app.route("/offers")
def offers():
    ports = Port.query.all()
    # best_spread = get_optimal_spread(ports)
    return render_template("offers.html", ports=ports)

@app.route(
    "/handle_transaction/<int:port_id>/<int:crew_id>/<string:item_id>/<string:action>",
    methods=["POST"],
)
def handle_transaction(port_id, crew_id, item_id, action):
    port = Port.query.get_or_404(port_id)
    crew = Crew.query.get_or_404(crew_id)

    price_mapping = {
        "rice": port.rice_price,
        "tea": port.tea_price,
        "wine": port.wine_price,
        "spice": port.spice_price,
        "gold": port.gold_price,
        "canon": port.canon_price,
        "diamonds": port.diamonds_price,
    }

    quantity_mapping = {
        "rice": crew.rice_count,
        "tea": crew.tea_count,
        "wine": crew.wine_count,
        "spice": crew.spice_count,
        "gold": crew.gold_count,
        "canon": crew.canon_count,
        "diamonds": crew.diamonds_count,
    }

    if item_id not in price_mapping:
        return "Invalid item", 400

    item_price = price_mapping[item_id]
    item_count = quantity_mapping[item_id]

    if action == "buy":
        if check_low_balance(crew, item_price) and check_low_carry(crew):
            crew.balance -= item_price
            setattr(crew, f"{item_id}_count", item_count + 1)
            crew.current_carry += 1

            if item_id == "canon" and not crew.is_pirate:
                crew.is_pirate = True
                db.session.commit()
        else:
            return render_template("crew_operation.html", crew=crew, port=port)
    elif action == "sell":
        if check_item_count(item_count) and check_empty_storage(crew):
            crew.balance += item_price
            setattr(crew, f"{item_id}_count", item_count - 1)
            crew.current_carry -= 1

            if item_id == "canon" and crew.canon_count == 1:
                crew.is_pirate = False 
                db.session.commit()
        else:
            return render_template("crew_operation.html", crew=crew, port=port)

    else:
        render_template("errors/404.html")

    db.session.commit()

    flash(f"Transaction successful: {action} {item_id} for {item_price}$")
    return render_template("crew_operation.html", crew=crew, port=port)


@app.route("/tasks")
def tasks():
    return render_template("tasks.html")

@app.route("/steal", methods=["POST"])
def steal():
    crew1_name = request.form.get("crew1")
    crew2_name = request.form.get("crew2")
    percentage = request.form.get("percentage", type=int)

    crew1 = Crew.query.filter_by(name=crew1_name).first()
    crew2 = Crew.query.filter_by(name=crew2_name).first()

    if not crew1 or not crew2 or not percentage:
        return render_template("errors/404.html"), 404

    if crew1.canon_count == crew2.canon_count:
        flash("Both users are pirates with an equal number of canons!")
        return redirect(request.referrer or '/')
    elif crew2.canon_count > crew1.canon_count:
        flash("Attacked crew has a higher number of canons!")
        return redirect(request.referrer or '/')

    loot = int((crew2.balance * percentage) / 100)  # Correct percentage calculation

    crew2.balance -= loot
    crew1.balance += loot

    db.session.commit()

    flash(f"{loot}$ were stolen!")
    return redirect(request.referrer or '/')