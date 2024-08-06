#!/usr/bin/python3
""" module that contains routes endpoints for Review
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route(
                'places/<place_id>/reviews',
                methods=['GET'],
                strict_slashes=False)
def get_all_reviews(place_id):
    """ get all reviews
    """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    review_objs = place_obj.reviews
    result = []
    for review in review_objs:
        result.append(review.to_dict())
    return jsonify(result), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ get review by id
    """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    result = review_obj.to_dict()
    return jsonify(result), 200


@app_views.route(
                '/reviews/<review_id>',
                methods=['DELETE'],
                strict_slashes=False)
def delete_review(review_id):
    """ delete review by id
    """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    storage.delete(review_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
                'places/<place_id>/reviews',
                methods=['POST'],
                strict_slashes=False)
def create_review(place_id):
    """ create new review
    """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    obj_dict = request.get_json()
    if not obj_dict:
        abort(400, description="Not a JSON")

    if 'user_id' not in obj_dict:
        abort(400, description="Missing user_id")

    user_obj = storage.get(User, obj_dict.get("user_id"))

    if not user_obj:
        abort(404)

    if 'text' not in obj_dict:
        abort(400, description="Missing text")

    new_review = Review(**obj_dict)
    setattr(new_review, 'user_id', obj_dict.get("user_id"))
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ update review
    """
    # check if object exists
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    update_dict = request.get_json()
    if not update_dict:
        abort(400, description="Not a JSON")
    for key, value in update_dict.items():
        if key not in [
                        "id",
                        "created_at",
                        "updated_at",
                        "place_id",
                        "user_id"]:
            setattr(review_obj, key, value)

    storage.save()
    return jsonify(review_obj.to_dict()), 200
