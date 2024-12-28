from flask import flash, render_template

def check_low_balance(crew, port, item_price):
    if crew.balance < item_price:
        flash("Insufficient funds!", "warning")
        return render_template("crew_operation.html", crew=crew, port=port)

def check_low_carry(crew, port):
    if crew.max_carry < crew.current_carry + 1:
        flash("Insufficient storage!", "warning")
        return render_template("crew_operation.html", crew=crew, port=port)

def check_empty_storage(crew, port):
    if crew.current_carry == 0:
        flash("Empty storage!", "warning")
        return render_template("crew_operation.html", crew=crew, port=port)

def check_item_count(crew, port, item_count):
    if item_count == 0:
        flash("Item not in storage!", "warning")
        return render_template("crew_operation.html", crew=crew, port=port)