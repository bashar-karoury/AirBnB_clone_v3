#!/usr/bin/python3
""" module that contains routes endpoints for City
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route(
                'states/<state_id>/cities',
                methods=['GET'],
                strict_slashes=False)
def get_all_cities(state_id):
    """ get all cities
    """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    city_objs = state_obj.cities
    result = []
    for city in city_objs:
        result.append(city.to_dict())
    return jsonify(result), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ get city by id
    """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    result = city_obj.to_dict()
    return jsonify(result), 200


@app_views.route(
                '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ delete city by id
    """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
                'states/<state_id>/cities',
                methods=['POST'],
                strict_slashes=False)
def create_city(state_id):
    """ create new city
    """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    obj_dict = request.get_json()
    if not obj_dict:
        abort(400, description="Not a JSON")

    if 'name' not in obj_dict:
        abort(400, description="Missing name")

    new_city = City(**obj_dict)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ update city
    """
    # check if object exists
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    update_dict = request.get_json()
    if not update_dict:
        abort(400, description="Not a JSON")
    for key, value in update_dict.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city_obj, key, value)

    storage.save()
    return jsonify(city_obj.to_dict()), 200
