from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, logout_user, current_user, login_user
from icecream import ic
import logging

from logging.handlers import RotatingFileHandler

db = SQLAlchemy()

def setup_logging(app):
    # Set the log level
    app.logger.setLevel(logging.DEBUG)

    # Create a file handler that logs debug and higher level messages
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = logging.Formatter(
        'Date: %(asctime)s, LogLvl: %(levelname)s, %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the app's logger
    app.logger.addHandler(handler)