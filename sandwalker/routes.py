"""Sandwalker routes."""

from flask import Blueprint
from flask import abort, current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_minify import minify
from sassutils.wsgi import SassMiddleware

from .models import TimelineEntry
from .forms import ViewPocketAccountHistoryForm
from .pocket import make_entries_by_month


sandwalker = Blueprint(
    'sandwalker', __name__, template_folder='templates',
    static_folder='static', static_url_path='/static/'
)


@sandwalker.route('/', methods=['GET', 'POST'])
def home():
    last = TimelineEntry.query.order_by(TimelineEntry.id.desc()).limit(1).first()
    current_height = last.block if last else 'unknown'

    return render_template('home.html', current_height=current_height)


@sandwalker.route('/explorer', methods=['GET', 'POST'])
def explorer(account=None):

    # Redirect to the nice URL /explorer/<account>/
    form = ViewPocketAccountHistoryForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for('sandwalker.explore', account=form.account.data))
    
    return render_template('explorer.html', form=form)


@sandwalker.route('/explore/<account>', methods=['GET'])
def explore(account):

    entries_by_month = []
    total = None
    count = None

    if account:
        account = account.lower()
        entries = TimelineEntry.query.filter(TimelineEntry.account == account).all()

        if len(entries) == 0:
            flash('No reward were found for {0}'.format(account), 'error')

        count, total, entries_by_month = make_entries_by_month(entries)
    
    return render_template(
        'explore.html', account=account, entries_by_month=entries_by_month, total=total, count=count)


@sandwalker.route('/about')
def about():
    return render_template('about.html')


@sandwalker.route('/resources', methods=['GET'])
def resources():
    return render_template('resources.html')


@sandwalker.route('/api/rewards/<account>', methods=['GET'])
def api_rewards(account):
    result = {'error': None}
    if not account:
        result['error'] = 'Invalid account parameters'
        return jsonify(result), 503

    account = account.lower()
    entries = TimelineEntry.query.filter(TimelineEntry.account == account).all()
    if len(entries) == 0:
        result['error'] = 'No rewards found for {0}'.format(account)
        return jsonify(result), 404

    count, total, entries_by_month = make_entries_by_month(entries)

    result['count'] = count
    result['total'] = total
    result['all_entries'] = entries_by_month

    return jsonify(result), 200


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
