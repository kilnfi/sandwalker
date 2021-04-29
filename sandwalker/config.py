"""SandWalker base config.
"""

class ConfigClass(object):
    """SandWalker Flask application config."""

    SECRET_KEY = ''
    SERVER_NAME = '127.0.0.1:5000'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/sandwalker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_APP_NAME = "Sandwakler"
    TEMPLATES_AUTO_RELOAD = False
    TESTING = False
    WTF_CSRF_ENABLED = True
