from datetime import datetime, timezone
from hashlib import md5
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from src import db


class Port(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    pirate = db.Column(db.Boolean, default=False, nullable=False)
    rice_price = db.Column(db.Integer, nullable=False)
    tea_price = db.Column(db.Integer, nullable=False)
    wine_price = db.Column(db.Integer, nullable=False)
    spice_price = db.Column(db.Integer, nullable=False)
    gold_price = db.Column(db.Integer, nullable=False)
    diamonds_price = db.Column(db.Integer, nullable=False)
    slaves_price = db.Column(db.Integer, nullable=False)

class Crew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    color = db.Column(db.String(32), nullable=False)