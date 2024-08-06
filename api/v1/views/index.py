#!/usr/bin/python3
""" module that contains routes of view Blueprint
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """ returns status of app
    """
    return jsonify({"status": "OK"})
