#!/usr/bin/python3
""" module that contains routes endpoints for State
"""
from api.v1.views import app_views
from flask import jsonify, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """ get all states
    """
    state_objs = storage.all(State)
    result = []
    for state in state_objs:
        result.append(state_objs[state].to_dict())
    return jsonify(result), 200


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ get state by id
    """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    result = state_obj.to_dict()
    return jsonify(result), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ delete state by id
    """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    storage.delete(state_obj)
    return jsonify({}), 200
