from datetime import datetime, timedelta, timezone

from flask import flash, g, jsonify, redirect, render_template, request, url_for

from src import app, db
from src.forms import NewCrewForm, NewPortForm
from src.models import Crew, GameTimer, Port
from src.utils import *


@app.context_processor
def inject_timer_status():
    timer = GameTimer.query.first()
    if timer:
        now = datetime.now(timezone.utc)
        if timer.end_time.tzinfo is None:
            timer.end_time = timer.end_time.replace(tzinfo=timezone.utc)
        seconds_left = int((timer.end_time - now).total_seconds())
        game_over = seconds_left <= 0
    else:
        seconds_left = 0
        game_over = False
    return dict(game_over=game_over, seconds_left=seconds_left)

@app.route("/start_timer", methods=["POST"])
def start_timer():
    minutes = request.form.get("minutes", type=int)
    if minutes:
        now = datetime.now(timezone.utc)
        end_time = now + timedelta(minutes=minutes)
        timer = GameTimer.query.first()
        if timer:
            timer.start_time = now
            timer.end_time = end_time
        else:
            timer = GameTimer(start_time=now, end_time=end_time)
            db.session.add(timer)
        db.session.commit()
        flash("Timer started!", "success")
    else:
        flash("Please enter a valid number of minutes.", "danger")
    return redirect(url_for("admin"))

@app.route("/timer_status")
def timer_status():
    timer = GameTimer.query.first()
    if timer:
        now = datetime.now(timezone.utc)
        if timer.end_time.tzinfo is None:
            timer.end_time = timer.end_time.replace(tzinfo=timezone.utc)
        seconds_left = int((timer.end_time - now).total_seconds())
        is_active = seconds_left > 0
        if seconds_left < 0:
            seconds_left = 0
        return jsonify({"seconds_left": seconds_left, "is_active": is_active})
    else:
        return jsonify({"seconds_left": 0, "is_active": False})

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

@app.route("/results", methods=["GET", "POST"])
def results():
    timer = GameTimer.query.first()
    if timer:
        timer.end_time = datetime.now(timezone.utc) + timedelta(hours=1)
        db.session.commit()
    flash("Game over reset!", "success")

    crews = Crew.query.order_by(Crew.balance.desc()).all()
    return render_template("results.html", title="Results", crews=crews)

@app.route("/new_game", methods=["GET", "POST"])
def new_game():
    timer = GameTimer.query.first()
    if timer:
        timer.end_time = datetime.now(timezone.utc) + timedelta(hours=1)
        db.session.commit()
    flash("New game started!", "success")
    return render_template("index.html")

@app.route("/services", methods=["GET", "POST"])
def services():
    crews = Crew.query.all()
    
    if request.method == "POST":
        action = request.form.get('action')
        
        if action == "give":
            crew_name = request.form.get('give_crew')
            amount = int(request.form.get('give_amount'))

            crew = Crew.query.filter_by(name=crew_name).first()
            crew.balance += amount
            db.session.commit()

            flash(f"Given {amount} to {crew_name}", "success")
            
        elif action == "take":
            crew_name = request.form.get('take_crew')
            amount = int(request.form.get('take_amount'))

            crew = Crew.query.filter_by(name=crew_name).first()
            crew.balance -= amount
            db.session.commit()

            flash(f"Taken {amount} from {crew_name}", "success")
            
        return redirect(url_for('services'))
    
    return render_template("services.html", crews=crews)

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
        ports = Port.query.all()
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

    loot = int((crew2.balance * percentage) / 100)

    crew2.balance -= loot
    crew1.balance += loot

    db.session.commit()

    flash(f"{loot}$ were stolen!")
    return redirect(request.referrer or '/')
