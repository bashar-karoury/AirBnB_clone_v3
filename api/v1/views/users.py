#!/usr/bin/python3
""" module that contains routes endpoints for User
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ get all users
    """
    user_objs = storage.all(User)
    result = []
    for user in user_objs:
        result.append(user_objs[user].to_dict())
    return jsonify(result), 200


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ get user by id
    """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    result = user_obj.to_dict()
    return jsonify(result), 200


@app_views.route(
                '/users/<user_id>',
                methods=['DELETE'],
                strict_slashes=False)
def delete_user(user_id):
    """ delete user by id
    """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ create new user
    """
    obj_dict = request.get_json()

    if not obj_dict:
        abort(400, description="Not a JSON")

    if 'email' not in obj_dict:
        abort(400, description="Missing email")
    if 'password' not in obj_dict:
        abort(400, description="Missing password")

    new_user = User(**obj_dict)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ update user
    """
    # check if object exists
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    update_dict = request.get_json()
    if not update_dict:
        abort(400, description="Not a JSON")
    for key, value in update_dict.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user_obj, key, value)

    storage.save()
    return jsonify(user_obj.to_dict()), 200
