# -*- coding: utf-8 -*-
import os

class Config(object):
    SECRET_KEY = 'akV5JQZyKxcwdOTs2ZSK+PeM/r2fOzwguKKfadWJg/4='
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    LOG_FILE = 'eveask.log'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'GeHzBFbt3xps3zpCr33x5bKNiq+xGsL1FKdD1ZGJyI8='
    SECURITY_TRACKABLE = True


class ProdConfig(Config):
    CACHE_TYPE = 'simple'
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://eveask:eveask@db.local/eveask' # DB URL
    REDIS = '127.0.0.1'


class DevConfig(Config):
    CACHE_TYPE = 'simple'
    DEBUG = True
    DB_NAME = 'eveask.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    SQLALCHEMY_ECHO = True
    REDIS = '127.0.0.1'

