"""SandWalker custom forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class ViewPocketAccountHistoryForm(FlaskForm):
    account = StringField('account', [DataRequired()])


class ReportForm(FlaskForm):
    accounts = TextAreaField(
        'accounts', [DataRequired()], render_kw={'class': 'form-control', 'rows': 10})
