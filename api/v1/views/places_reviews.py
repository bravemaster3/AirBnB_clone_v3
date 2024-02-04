#!/usr/bin/python3
"""
This module handles all default RESTful API actions related to reviews
"""
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_reviews(place_id):
    """get a list of all reviews of a place or creates a new Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        all_reviews = place.reviews
        reviews_list = [obj.to_dict() for obj in all_reviews]
        return jsonify(reviews_list)

    if request.method == 'POST':
        review_dict = request.get_json()
        if not review_dict:
            abort(400, 'Not a JSON')
        if 'user_id' not in review_dict:
            abort(400, 'Missing user_id')
        if not storage.get(User, review_dict['user_id']):
            abort(404)
        if 'text' not in review_dict:
            abort(400, 'Missing text')
        new_review = Review(**review_dict)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review_by_id(review_id):
    """get, updates or delete review with a specific id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        req_json = request.json
        for key in req_json.keys():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(review, key, req_json[key])
        storage.save()
        return jsonify(review.to_dict()), 200
