# -*- coding: utf-8 -*-
from flask import render_template
from jinja2 import Markup
from .app import app


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.context_processor
def inject_icon():
    def icon(icon_name):
        return Markup('<i class="fa fa-{icon}"></i>'.format(icon=icon_name))
    return dict(icon=icon)
