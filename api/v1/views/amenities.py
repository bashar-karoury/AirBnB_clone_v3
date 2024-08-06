#!/usr/bin/python3
""" module that contains routes endpoints for Amenity
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ get all amenities
    """
    amenity_objs = storage.all(Amenity)
    result = []
    for amenity in amenity_objs:
        result.append(amenity_objs[amenity].to_dict())
    return jsonify(result), 200


@app_views.route(
                '/amenities/<amenity_id>',
                methods=['GET'],
                strict_slashes=False)
def get_amenity(amenity_id):
    """ get amenity by id
    """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    result = amenity_obj.to_dict()
    return jsonify(result), 200


@app_views.route(
                '/amenities/<amenity_id>',
                methods=['DELETE'],
                strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete amenity by id
    """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
                '/amenities',
                methods=['POST'],
                strict_slashes=False)
def create_amenity():
    """ create new amenity
    """
    obj_dict = request.get_json()

    if not obj_dict:
        abort(400, description="Not a JSON")

    if 'name' not in obj_dict:
        abort(400, description="Missing name")

    new_amenity = Amenity(**obj_dict)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
                '/amenities/<amenity_id>',
                methods=['PUT'],
                strict_slashes=False)
def update_amenity(amenity_id):
    """ update amenity
    """
    # check if object exists
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    update_dict = request.get_json()
    if not update_dict:
        abort(400, description="Not a JSON")
    for key, value in update_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, value)

    storage.save()
    return jsonify(amenity_obj.to_dict()), 200
