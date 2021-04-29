"""SandWalker custom forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ViewPocketAccountHistoryForm(FlaskForm):
    account = StringField('account', [DataRequired()])
