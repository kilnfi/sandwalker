"""SandWalker base config.
"""

import os


class ConfigClass(object):
    """SandWalker Flask application config."""

    SERVER_NAME = os.getenv('VIRTUALHOST', default='127.0.0.1:5000')    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:////data/timeline.db?mode=ro')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_APP_NAME = "The Sand Walker"
    TEMPLATES_AUTO_RELOAD = False
    TESTING = False
    WTF_CSRF_ENABLED = False

    # This key is not really important as the Sand Walker doesn't use
    # sessions. If you customize it to have session, you probably want
    # to edit the docker-compose file to override this key.
    SECRET_KEY = os.getenv('SECRET_KEY', default='w3jKh4NQiqlRyVN+FZb+wAw3jKh4NQiqlRyV')
