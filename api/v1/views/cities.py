#!/usr/bin/python3
"""
This module handles all default RESTful API actions related to cities
"""
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_cities(state_id):
    """get a list of all cities of a state or creates a new City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        all_cities = state.cities
        cities_list = [obj.to_dict() for obj in all_cities]
        return cities_list

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        new_city = City(state_id=state_id, name=request.json['name'])
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_by_id(city_id):
    """get, updates or delete city with a specific id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        return city.to_dict()

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        req_json = request.json
        for key in req_json.keys():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, req_json[key])
        storage.save()
        return jsonify(city.to_dict()), 200
