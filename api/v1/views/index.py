#!/usr/bin/python3
"""
This module contains the index
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """returns the status of the api"""
    return jsonify({"status": "OK"})
