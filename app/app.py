import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo


application = Flask(__name__)

application.config["MONGO_URI"] = (
    'mongodb://' + os.environ['MONGODB_USERNAME'] +
    ':' + os.environ['MONGODB_PASSWORD'] + '@' +
    os.environ['MONGODB_HOSTNAME'] +
    ':27017/' + os.environ['MONGODB_DATABASE']
    )

mongo = PyMongo(application)
db = mongo.db


# main page route
@application.route('/')
def index():
    return jsonify(
        status=True,
        message=(
            'Welcome to the DVD rental '
            'service that is hopefully functional!'
    )


# To do route. GET API.
@application.route('/customers')
def customers():
    _todos = db.customers.find()

    item = {}
    data = []
    for todo in _todos:
        item = {
            'id': str(todo['_id']),
            'todo': todo['todo']
        }
        data.append(item)

    return jsonify(
        status=True,
        data=data
    )

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(
        host='0.0.0.0', port=ENVIRONMENT_PORT,
        debug=ENVIRONMENT_DEBUG
    )
