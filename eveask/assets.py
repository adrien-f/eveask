# -*- coding: utf-8 -*-
from flask.ext.assets import Bundle

common_css = Bundle(
    "../bower_components/bootstrap/dist/css/bootstrap.min.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/common.css"
)

common_js = Bundle(
    "../bower_components/jquery/jquery.min.js",
    Bundle(
        "js/script.js",
        filters="jsmin"
    ),
    output="public/js/common.js"
)
