#!/usr/bin/python3
"""
This module contains some init routines
"""
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
