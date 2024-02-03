#!/usr/bin/python3
"""
This module handles all default RESTful API actions related to states
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import request, abort, jsonify, make_response


@app_views.route('/states/', methods=['GET', 'POST'])
def all_states():
    """get a list of all states or creates a new state"""
    if request.method == 'GET':
        all_states = storage.all(State)
        states_list = [obj.to_dict() for obj in all_states.values()]
        return states_list

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        new_state = State(name=request.json['name'])
        storage.new(new_state)
        storage.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state_by_id(state_id):
    """get, updates or delete state with a specific id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        return state.to_dict()

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        req_json = request.json
        for key in req_json.keys():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, req_json[key])
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
