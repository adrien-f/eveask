# -*- coding: utf-8 -*-
import os

class Config(object):
    SECRET_KEY = 'b33e65d91409ca5d8a47704efc6e4c5f'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    LOG_FILE = 'eveask.log'


class ProdConfig(Config):
    CACHE_TYPE = 'simple'
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://eveask:eveask@db.local/eveask' # DB URL


class DevConfig(Config):
    CACHE_TYPE = 'simple'
    DEBUG = True
    DB_NAME = 'eveask.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    SQLALCHEMY_ECHO = True

