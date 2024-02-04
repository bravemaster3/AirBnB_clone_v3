#!/usr/bin/python3
"""
This module handles all default RESTful API actions related to amenities
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_amenities():
    """get a list of all amenities or creates a new amenity"""
    if request.method == 'GET':
        all_amenities = storage.all(Amenity)
        amenities_list = [obj.to_dict() for obj in all_amenities.values()]
        return jsonify(amenities_list)

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        new_amenity = Amenity(name=request.json['name'])
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """get, updates or delete amenity with a specific id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        req_json = request.json
        for key in req_json.keys():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, req_json[key])
        storage.save()
        return jsonify(amenity.to_dict()), 200
