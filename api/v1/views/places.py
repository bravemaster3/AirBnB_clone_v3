#!/usr/bin/python3
"""
This module handles all default RESTful API actions related to places
"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_places(city_id):
    """get a list of all places of a city or creates a new City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        all_places = city.places
        places_list = [obj.to_dict() for obj in all_places]
        return jsonify(places_list)

    if request.method == 'POST':
        place_dict = request.get_json()
        if not place_dict:
            abort(400, 'Not a JSON')
        if 'user_id' not in place_dict:
            abort(400, 'Missing user_id')
        if not storage.get(User, place_dict['user_id']):
            abort(404)
        if 'name' not in place_dict:
            abort(400, 'Missing name')
        new_place = Place(**place_dict)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_by_id(place_id):
    """get, updates or delete place with a specific id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        req_json = request.json
        for key in req_json.keys():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(place, key, req_json[key])
        storage.save()
        return jsonify(place.to_dict()), 200
