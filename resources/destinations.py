import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user

destination = Blueprint('destinations', 'destination')

@destination.route('/', methods=["GET"])
def get_all_destinations():
    try:
        destinations = [model_to_dict(destination) for destination in current_user.destinations]
        print(destinations)
        return jsonify(
            data=destinations,
            status={"code": 201, "message": "Success"}
        )
    except models.DoesNotExist:
        return jsonify(
            data={},
            status={"code": 401, "message": "Error getting the resources"}
        )

@destination.route('/', methods=["POST"])
def create_destinations():
    payload = request.get_json()
    print(type(payload), 'payload')
    destination = models.Destination.create(name=payload['name'], trip=payload['destination.trip_id'])
    print(destination.__dict__)
    print(dir(destination))
    print(model_to_dict(destination), 'model_to_dict')
    destination_dict = model_to_dict(destination)
    return jsonify(
        data=destination_dict,
        status={"code": 201, "message": "Success"}
    )
