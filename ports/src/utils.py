from flask import flash, render_template


def check_low_balance(crew, item_price):
    if crew.balance < item_price:
        flash("Insufficient funds!", "warning")
        return False
    return True

def check_low_carry(crew):
    if crew.max_carry < crew.current_carry + 1:
        flash("Insufficient storage!", "warning")
        return False
    return True

def check_empty_storage(crew):
    if crew.current_carry == 0:
        flash("Empty storage!", "warning")
        return False
    return True

def check_item_count(item_count):
    if item_count == 0:
        flash("Item not in storage!", "warning")
        return False
    return True

def get_optimal_spread(ports):
    pass
