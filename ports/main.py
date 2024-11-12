import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from src import app

# app = Flask(__name__)

# db_uri = os.environ.get('DATABASE_URI')
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
# db = SQLAlchemy(app)


# if __name__ == '__main__':
#     app.run()