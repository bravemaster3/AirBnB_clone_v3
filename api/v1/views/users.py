#!/usr/bin/python3
"""
This module handles all default RESTful API actions related to users
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_users():
    """get a list of all users or creates a new user"""
    if request.method == 'GET':
        all_users = storage.all(User)
        users_list = [obj.to_dict() for obj in all_users.values()]
        return users_list

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'email' not in request.get_json():
            abort(400, 'Missing email')
        if 'password' not in request.get_json():
            abort(400, 'Missing password')
        new_user = User(email=request.json['email'],
                        password=request.json['password'])
        if 'first_name' in request.get_json():
            setattr(new_user, 'first_name', request.json['first_name'])
        if 'last_name' in request.get_json():
            setattr(new_user, 'last_name', request.json['last_name'])
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_by_id(user_id):
    """get, updates or delete user with a specific id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return user.to_dict()

    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        req_json = request.json
        for key in req_json.keys():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, req_json[key])
        storage.save()
        return jsonify(user.to_dict()), 200
