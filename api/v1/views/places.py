#!/usr/bin/python3
""" module that contains routes endpoints for Place
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models import storage


@app_views.route(
                'cities/<city_id>/places',
                methods=['GET'],
                strict_slashes=False)
def get_all_places(city_id):
    """ get all places
    """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    place_objs = city_obj.places
    result = []
    for place in place_objs:
        result.append(place.to_dict())
    return jsonify(result), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ get place by id
    """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    result = place_obj.to_dict()
    return jsonify(result), 200


@app_views.route(
                '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ delete place by id
    """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
                'cities/<city_id>/places',
                methods=['POST'],
                strict_slashes=False)
def create_place(city_id):
    """ create new place
    """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    obj_dict = request.get_json()
    if not obj_dict:
        abort(400, description="Not a JSON")

    if 'user_id' not in obj_dict:
        abort(400, description="Missing user_id")

    if 'name' not in obj_dict:
        abort(400, description="Missing name")

    new_place = Place(**obj_dict)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ update place
    """
    # check if object exists
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    update_dict = request.get_json()
    if not update_dict:
        abort(400, description="Not a JSON")
    for key, value in update_dict.items():
        if key not in ["id", "created_at", "updated_at", "city_id", "user_id"]:
            setattr(place_obj, key, value)

    storage.save()
    return jsonify(place_obj.to_dict()), 200
