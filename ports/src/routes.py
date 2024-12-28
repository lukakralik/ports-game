from flask import flash, redirect, render_template, url_for

from src import app, db
from src.forms import NewCrewForm, NewPortForm
from src.models import Crew, Port
from src.utils import *


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
            slaves_price=form.slaves.data,
        )
        db.session.add(port)
        db.session.commit()
        flash("New port has been initialized successfully.", "success")
        return redirect(url_for("admin"))
    return render_template("admin/new_port.html", form=form)


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
            slaves_count=0,
            diamonds_count=0,
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
    return render_template("crew_operation.html", port=port, crew=crew)


@app.route("/offers")
def offers():
    return render_template("offers.html")

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
        "slaves": port.slaves_price,
        "diamonds": port.diamonds_price,
    }

    quantity_mapping = {
        "rice": crew.rice_count,
        "tea": crew.tea_count,
        "wine": crew.wine_count,
        "spice": crew.spice_count,
        "gold": crew.gold_count,
        "slaves": crew.slaves_count,
        "diamonds": crew.diamonds_count,
    }

    if item_id not in price_mapping:
        return "Invalid item", 400

    item_price = price_mapping[item_id]
    item_count = quantity_mapping[item_id]

    if action == "buy":
        check_low_balance(crew, port, item_price)
        check_low_carry(crew, port)

        crew.balance -= item_price
        setattr(crew, f"{item_id}_count", item_count + 1)
        crew.current_carry += 1
    elif action == "sell":
        check_empty_storage(crew, port)

        if item_count:
            crew.balance += item_price
            setattr(crew, f"{item_id}_count", item_count - 1)
            crew.current_carry -= 1
        else:
            flash("Item not in storage!", "warning")
            return render_template("crew_operation.html", crew=crew, port=port)

    else:
        render_template("errors/404.html")

    db.session.commit()

    flash(f"Transaction successful: {action} {item_id} for {item_price}$")
    return render_template("crew_operation.html", crew=crew, port=port)


@app.route("/tasks")
def tasks():
    return render_template("tasks.html")


# view function mapped onto urls / and /index
