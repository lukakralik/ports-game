from flask import render_template

from src import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404 # returned rendered page and status code along


@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback() # return to latest DB write
    return render_template("500.html"), 500