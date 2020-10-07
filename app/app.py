import os
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from datetime import datetime as dt

application = Flask(__name__)

application.config["MONGO_URI"] = (
    'mongodb://' + os.environ['MONGODB_USERNAME'] +
    ':' + os.environ['MONGODB_PASSWORD'] + '@' +
    os.environ['MONGODB_HOSTNAME'] +
    ':27017/' + os.environ['MONGODB_DATABASE']
    )

mongo = PyMongo(application)
db = mongo.db

# Note: all APIs that return data should have a limit and offset.
# not implemented here.


# main page route
@application.route('/')
def index():
    return jsonify(
        status=True,
        message=(
            'I am here and there and everywhere.'
        )
    )


@application.route('/customers')
def get_all_customers():
    items = db.customers.find({}, {'_id': 1, 'First Name': 1, 'Last Name': 1})

    # This will load all the data. If the dataset is large we will
    # load chunks. 600 datapoints is probably ok for now.
    data = list(items)
    return jsonify(
        status=True,
        data=data
    )


@application.route('/customer/<customer_id>')
def get_customer(customer_id):
    # The manipulation of the data using Pandas
    # would be much easier, except that it will
    # take time to install it on Alpine.
    customer_info = db.customers.find_one(
        {'_id': int(customer_id)},
        {
            'First Name': 1, 'Last Name': 1,
            'Address': 1, 'City': 1, 'Country': 1,
        }
    )

    rentals = db.customers.find(
        {'_id': int(customer_id)},
        {
            'Rentals.Film Title': 1, 'Rentals.Rental Date': 1,
            'Rentals.Return Date': 1, 'Rentals.Payments.Amount': 1,
            '_id': 0
        }
    )

    # We could have used aggregation in the customers to calculate the time
    # difference.
    # Horrible code...
    films = []
    amounts = []
    rental_dates = []
    duration = []
    # firt for loop is one...
    for rental in rentals:
        for item in rental.get('Rentals'):
            rental_day = item.get('Rental Date')
            return_day = item.get('Return Date')
            films.append(item.get('Film Title'))
            amounts.append(item.get('Payments')[0]['Amount'])
            rental_dates.append(rental_day)
            duration_days = _calculate_days(rental_day, return_day)
            duration.append(duration_days)

    data = [{
        'customer': customer_info,
        'film_titles': films,
        'rental_dates': rental_dates,
        'amounts': amounts,
        'duration': duration

    }]

    if not customer_info:
        return jsonify(
            status=True,
            data=[]
        )

    return jsonify(
            data=data
    )


@application.route('/films')
def get_all_films():
    films = db.films.find(
        {},
        {
            '_id': 1, 'Title': 1, 'Category': 1, 'Rating': 1,
            'Description': 1, 'Rental Duration': 1
        }
    )

    if not films:
        return jsonify(
            status=True,
            data=[]
        )
    #
    return jsonify(
            status=True,
            data=list(films)
    )


@application.route('/film/<film_id>')
def get_film(film_id):

    # We need to filter rentals as well to get only the data required.
    # will do that if I have time.
    film = db.films.find_one(
        {'_id': int(film_id)},
    )

    if not film:
        return jsonify(
            status=True,
            data=[]
        )
    customers = db.customers.find(
        {'Rentals.Film Title': film.get('Title')},
        {'_id': 1, 'First Name': 1, 'Last Name': 1})

    data = {
        'film_details': film,
        'customers': list(customers)
    }

    return jsonify(
            status=True,
            data=data
    )


def _calculate_days(rental_datetime, return_datetime):
    time_format = '%Y-%m-%d %H:%M:%S'
    rental_datetime = rental_datetime.split('.')[0]
    return_datetime = return_datetime.split('.')[0]
    rental_datetime = dt.strptime(rental_datetime, time_format)
    return_datetime = dt.strptime(return_datetime, time_format)
    result = return_datetime - rental_datetime
    return result.days


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(
        host='0.0.0.0', port=ENVIRONMENT_PORT,
        debug=ENVIRONMENT_DEBUG
    )
