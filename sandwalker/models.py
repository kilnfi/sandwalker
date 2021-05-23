"""Sandwalker database models.
"""

from flask import current_app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class TimelineEntry(db.Model):
    __tablename__ = 'timeline'

    id = db.Column(db.Integer(), primary_key=True)
    account = db.Column(db.Text)
    block = db.Column(db.Integer())
    time = db.Column(db.DateTime())
    amount = db.Column(db.Integer())


def init_app(app):
    db.init_app(app)

    # We don't create the database here as we don't want to mess with
    # the permissions (the pocket node will create it in 644, which is
    # fine as we only need to read from it).
