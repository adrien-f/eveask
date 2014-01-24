# -*- coding: utf-8 -*-

from .app import app, db, ldaptools

"""Create models here"""

db.create_all()
