"""Sandwalker routes."""

from flask import Blueprint
from flask import abort, current_app, flash, redirect, render_template
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
        flash('Account {0} was found'.format(form.account), 'success')
    return render_template('home.html', form=form)


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
    
