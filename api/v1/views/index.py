#!/usr/bin/python3
""" module that contains routes of view Blueprint
"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
@app_views.route('/status')
def status():
    """ returns status of app
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    """ returns retrieves the number of each objects by type
    """
    classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}
    count_dict = {}
    for clss_name, clss in classes.items():
        count_dict[clss_name] = storage.count(clss)

    return jsonify(count_dict)





