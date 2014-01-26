# -*- coding: utf-8 -*-
import os
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment
from flask.ext.security import Security
from webassets.loaders import PythonLoader
from eveask import assets

app = Flask(__name__)

# The environment variable, either 'prod' or 'dev'
env = os.environ.get("EVEASK_ENV", "dev")

# Use the appropriate environment-specific settings
app.config.from_object('eveask.settings.{env}Config'.format(env=env.capitalize()))

app.config['ENV'] = env

db = SQLAlchemy(app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

from eveask.models import user_datastore  #  Circular imports FTW
security = Security(app, user_datastore)

# Register asset bundles
assets_env = Environment()
assets_env.init_app(app)
assets_loader = PythonLoader(assets)
for name, bundle in assets_loader.load_bundles().iteritems():
    assets_env.register(name, bundle)


# Set up logging
file_handler = RotatingFileHandler(app.config['LOG_FILE'])
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)
