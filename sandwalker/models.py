"""Sandwalker database models.
"""

from flask import current_app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class TimelineEntry(db.Model):
    __tablename__ = 'timeline'

    entry_id = db.Column(db.Integer, primary_key=True)
    timeline = db.Column(db.Text)
    block = db.Integer
    amount = db.Integer


def init_app(app):
    db.init_app(app)
    db.create_all()
