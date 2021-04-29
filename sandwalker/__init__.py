import os
import os.path

from sandwalkler import config
from flask import Flask

from . import models, routes, forms, config


def create_app():
    app = Flask(__name__)

    app.register_blueprint(routes.sandwalkler)

    app.config.from_object(config.ConfigClass)
    app.config.from_envvar('FLASK_ENV_CONFIG')

    with app.app_context():
        models.init_app(app)

    routes.init_app(app)

    return app
