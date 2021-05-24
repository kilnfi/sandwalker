import os
import os.path

from sandwalker import config
from flask import Flask

from . import models, routes, forms, config


def create_app():
    app = Flask(__name__)

    app.register_blueprint(routes.sandwalker)

    app.config.from_object(config.ConfigClass)

    with app.app_context():
        models.init_app(app)

    routes.init_app(app)

    return app
