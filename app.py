from sandwalker import create_app
from sandwalker import models
from ilock import ILock


def make_app():
    with ILock('sandwalker-init-lock'):
        app = create_app()
        with app.app_context():
            fixtures.init_app(app, models.db)
    return app


app = make_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
