#!/usr/bin/env python
import logging
import sys
import os
import subprocess
from flask.ext.script import Manager, Shell, Server
from flask.ext.assets import ManageAssets
from webassets.script import CommandLineEnvironment
from eveask.app import assets_env
from eveask.main import app

manager = Manager(app)
TEST_CMD = "nosetests"

def _make_context():
    '''Return context dict for a shell session so you can access
    app, db, and models by default.
    '''
    return {'app': app}


@manager.command
def test():
    '''Run the tests.'''
    status = subprocess.call(TEST_CMD, shell=True)
    sys.exit(status)

@manager.command
def clean_assets():
    log = logging.getLogger('webassets')
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.DEBUG)
    cmdenv = CommandLineEnvironment(assets_env, log)
    cmdenv.clean()

@manager.command
def build_assets():
    log = logging.getLogger('webassets')
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.DEBUG)
    cmdenv = CommandLineEnvironment(assets_env, log)
    cmdenv.build()

@manager.command
def watch_assets():
    log = logging.getLogger('webassets')
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.DEBUG)
    cmdenv = CommandLineEnvironment(assets_env, log)
    cmdenv.watch()


manager.add_command("runserver", Server(host='0.0.0.0', port=os.getenv('PORT', 5000), debug=True))
manager.add_command("shell", Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()
