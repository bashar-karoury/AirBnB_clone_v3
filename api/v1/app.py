#!/usr/bin/python3
"""contains the main app to run"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ returns a JSON-formatted 404 status code response"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def custom_400_error(error):
    """ responde with 400 error code with custorm message
    """
    response = jsonify({"error": error.description})
    response.status_code = 400
    return response


if __name__ == '__main__':
    HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
