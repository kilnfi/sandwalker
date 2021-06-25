"""Sandwalker routes."""

import csv
import datetime

from flask import Blueprint
from flask import abort, current_app, flash, jsonify, make_response, redirect, render_template, request, send_from_directory, url_for
from flask_minify import minify
from io import StringIO
from sassutils.wsgi import SassMiddleware
from sqlalchemy import and_, distinct, func, tuple_

from .models import db, TimelineEntry
from .forms import ReportForm, ViewPocketAccountHistoryForm
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


@sandwalker.route('/sandwalker-daily-dump.tar.gz', methods=['GET'])
def dump():
    return send_from_directory('/data', 'timeline-backup.db.tar.gz', as_attachment=True)


@sandwalker.route('/explorer', methods=['GET', 'POST'])
def explorer(account=None):

    # Redirect to the nice URL /explorer/<account>/
    form = ViewPocketAccountHistoryForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for('sandwalker.explore', account=form.account.data))

    return render_template('explorer.html', form=form)


def sanitize_accounts(accounts):
    splitters = [',', '\r', '\n', '\t', ';']
    for splitter in splitters:
        accounts = accounts.replace(splitter, ' ')
    result = []

    for account in accounts.split(' '):
        clean_account = account.lower().strip()
        if clean_account:
            result.append(clean_account)

    return result


@sandwalker.route('/reporter', methods=['GET', 'POST'])
def reporter():
    form = ReportForm(request.form) if request.method == 'POST' else ReportForm(request.args)
    accounts = None
    entries = None
    node_count = 0

    # This can come both from GET or POST, directly use it without
    # checking if the form is valid.
    accounts = sanitize_accounts(form.accounts.data)

    if len(accounts) == 0:
        if request.method == 'POST':
            flash('Invalid list of account identifiers (accepted format: csv, space separated, tab separated, ...)', 'error')
    else:
        query = db.session.query(
            func.strftime("%Y-%m-01", TimelineEntry.time),
            func.sum(TimelineEntry.amount)).filter(
                TimelineEntry.account.in_(accounts)).group_by(
                    func.strftime("%Y-%m-01", TimelineEntry.time))

        entries = query.all()
        node_count = len(accounts)

    return render_template('reporter.html', form=form, accounts=accounts, entries=entries, node_count=node_count)


@sandwalker.route('/csv/overview', methods=['POST'])
def export_csv_overview():
    form = ReportForm()

    fields = ['month', 'account', 'total_upkt']
    output = StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=fields)
    csv_writer.writeheader()

    if form.validate_on_submit():
        accounts = sanitize_accounts(form.accounts.data)
        query = db.session.query(
            func.strftime("%Y-%m-01", TimelineEntry.time),
            TimelineEntry.account,
            func.sum(TimelineEntry.amount)).filter(
                TimelineEntry.account.in_(accounts)).group_by(
                    func.strftime("%Y-%m-01", TimelineEntry.time),
                    TimelineEntry.account)

        entries = query.all()

        for entry in entries:
            csv_writer.writerow(
                {'month': entry[0], 'account': entry[1], 'total_upkt': float(entry[2])})

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = 'attachment; filename=pocket_monthly_report.csv'
    response.headers["Content-type"] = 'text/csv'

    return response


@sandwalker.route('/explore/<account>', methods=['GET'])
def explore(account):

    entries_by_month = []
    total = None
    count = None

    if account:
        account = account.lower().strip()
        entries = TimelineEntry.query.filter(TimelineEntry.account == account).all()

        if len(entries) == 0:
            flash('No reward were found for {0}'.format(account), 'error')

        count, total, entries_by_month = make_entries_by_month(entries)
    
    return render_template(
        'explore.html', account=account, entries_by_month=entries_by_month, total=total, count=count)


@sandwalker.route('/csv/account/<account>', methods=['GET'])
def export_csv_account(account):
    fields = ['block_time', 'block_height', 'reward_upkt']
    output = StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=fields)
    csv_writer.writeheader()

    account = account.lower()
    entries = TimelineEntry.query.filter(TimelineEntry.account == account).all()
    for entry in entries:
        csv_writer.writerow(
            {'block_time': entry.time, 'block_height': entry.block, 'reward_upkt': entry.amount})

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = 'attachment; filename={0}.csv'.format(account)
    response.headers["Content-type"] = 'text/csv'

    return response


@sandwalker.route('/about')
def about():
    return render_template('about.html')


@sandwalker.route('/resources', methods=['GET'])
def resources():
    return render_template('resources.html')


@sandwalker.route('/api/block', methods=['GET', 'POST'])
def api_block():
    req = request.json

    if 'block' not in req:
        return jsonify({'error': 'Invalid request: no block specified'}), 503
    block = req.get('block')

    result = []
    entries = TimelineEntry.query.filter(
        TimelineEntry.block == block).all()

    for entry in entries:
        result.append({
            'reward': entry.amount,
            'account': entry.account,
            'block': entry.block,
            'time': entry.time,
        })

    return jsonify(result), 200


@sandwalker.route('/api/rewards', methods=['GET', 'POST'])
def api_rewards():
    req = request.json

    if 'accounts' not in req:
        return jsonify({'error': 'Invalid request: no Pocket accounts specified'}), 503
    accounts = [a.lower().strip() for a in req['accounts']]

    start_date = req.get('start_date', '1970-01-01 00:00:00')
    end_date = req.get('end_date', datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    result = {'accounts': {}}

    for account in accounts:
        result['accounts'][account] = list()
        entries = TimelineEntry.query.filter(
            and_(
                TimelineEntry.account == account,
                TimelineEntry.time.between(start_date, end_date))).all()

        for entry in entries:
            result['accounts'][account].append({
                'reward': entry.amount,
                'block': entry.block,
                'time': entry.time,
            })

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
