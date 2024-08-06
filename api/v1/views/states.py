#!/usr/bin/python3
""" module that contains routes endpoints for State
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ get all states
    """
    state_objs = storage.all(State)
    result = []
    for state in state_objs:
        result.append(state_objs[state].to_dict())
    return jsonify(result), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ get state by id
    """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    result = state_obj.to_dict()
    return jsonify(result), 200


@app_views.route(
                '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ delete state by id
    """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ create new state
    """
    obj_dict = request.get_json()

    if not obj_dict:
        abort(400, description="Not a JSON")

    if 'name' not in obj_dict:
        abort(400, description="Missing name")

    new_state = State(**obj_dict)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ update state
    """
    # check if object exists
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    update_dict = request.get_json()
    if not update_dict:
        abort(400, description="Not a JSON")
    for key, value in update_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, value)

    storage.save()
    return jsonify(state_obj.to_dict()), 200
