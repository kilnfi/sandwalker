"""Sandwalker routes."""

from flask import Blueprint
from flask import abort, current_app, flash, redirect, render_template, url_for
from flask_minify import minify
from sassutils.wsgi import SassMiddleware

from .models import TimelineEntry
from .forms import ViewPocketAccountHistoryForm


sandwalker = Blueprint(
    'sandwalker', __name__, template_folder='templates',
    static_folder='static', static_url_path='/static/'
)


@sandwalker.route('/', methods=['GET', 'POST'])
def home():
    form = ViewPocketAccountHistoryForm()

    if form.validate_on_submit():
        return redirect(url_for('sandwalker.explorer', account=form.account.data))

    return render_template('home.html', form=form)


@sandwalker.route('/explorer/<account>', methods=['GET'])
def explorer(account):
    entries = TimelineEntry.query.filter(TimelineEntry.account == account).all()
    total = sum([entry.amount for entry in entries])
    count = len(entries)

    if len(entries) == 0:
        flash('No reward were found for {0}'.format(account), 'error')
    
    return render_template(
        'explorer.html', account=account,entries=entries, total=total, count=count)


@sandwalker.route('/about')
def about():
    return render_template('about.html')


@sandwalker.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='The page you requested was not found'), 404


@sandwalker.app_errorhandler(500)
def page_crashed(e):
    return render_template('error.html', error='Some mysterious internal error occurred'), 500


def init_app(app):
    # Custom JINJA2 filters
    @app.template_filter()
    def filter_errors(form_errors):
        errs = set()
        for key, values in form_errors.items():
            for err in values:
                errs.add(err)
        return list(errs)
    app.jinja_env.filters['filter_errors'] = filter_errors

    # CSS/JS minimify and SASS compile.
    minify(
        app=app, html=True, js=True, cssless=True,
        script_types=['text/javascript'], bypass=['.*\\.min\\.js'])

    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'sandwalker': ('static/sass', 'static/css', '/static/css')
    })
    
