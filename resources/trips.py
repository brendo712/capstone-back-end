import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user

trip = Blueprint('trips', 'trip')

@trip.route('/', methods=["GET"])
def get_all_trips():
    try:
        trips = [model_to_dict(trip) for trip in current_user.trips]
        print(trips)
        return jsonify(
            data=trips,
            status={"code": 201, "message": "Success"}
        )
    except models.DoesNotExist:
        return jsonify(
            data={},
            status={"code": 401, "message": "Error getting the resources"}
        )

@trip.route('/', methods=["POST"])
def create_trips():
    payload = request.get_json()
    print(type(payload), 'payload')
    trip =models.Trip.create(title=payload['title'], author=current_user.id, trip_length=payload['trip_length'])
    print(trip.__dict__)
    print(dir(trip))
    print(model_to_dict(trip), 'model_to_dict')
    trip_dict = model_to_dict(trip)
    return jsonify(
        data=trip_dict,
        status={"code": 201, "message": "Success"}
    )

@trip.route('/<id>', methods=["GET"])
def get_one_trip(id):
    trip = models.Trip.get_by_id(id)
    return jsonify(
        data=model_to_dict(trip),
        status={"code": 200, "message": "Success"}
    )

@trip.route('/<id>', methods=["PUT"])
def update_trip(id):
    payload = request.get_json()
    query = models.Trip.update(**payload).where(models.Trip.id == id)
    query.execute()
    trip = model_to_dict(models.Trip.get_by_id(id))
    return jsonify(
        data=trip,
        status={"code": 200, "message": "Success"}
    )

@trip.route('/<id>', methods=["DELETE"])
def delete_trip(id):
    delete_query = models.Trip.delete().where(models.Trip.id == id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
        data={},
        message="Successfully deleted {} trip with id {}".format(num_of_rows_deleted, id),
        status={"code": 200}
    )    
