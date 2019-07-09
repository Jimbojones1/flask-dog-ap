import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
api = Blueprint('api', 'api', url_prefix='/api/v1')


@api.route('/', methods=["GET"])
def get_all_dogs():
    ## find the dogs and change each one to a dictionary into a new array
    dogs = [model_to_dict(dog) for dog in models.Dog.select()]
    print(dogs)
    return jsonify(dogs)


@api.route('/', methods=["POST"])
def create_dogs():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')
    dog = models.Dog.create(**payload)
    ## see the object
    print(dog.__dict__)
    ## Look at all the methods
    print(dir(dog))
    # Change the model to a dict
    print(model_to_dict(dog), 'model to dict')

    return jsonify(model_to_dict(dog))

@api.route('/<id>', methods=["GET"])
def get_one_dog(id):
    print(id, 'reserved word?')
    dog = models.Dog.get_by_id(id)
    print(dog.__dict__)
    return jsonify(model_to_dict(dog))

@api.route('/<id>', methods=["PUT"])
def update_dog(id):
    payload = request.get_json()
    query = models.Dog.update(**payload).where(models.Dog.id==id)
    query.execute()
    return jsonify(model_to_dict(models.Dog.get_by_id(id)))

@api.route('/<id>', methods=["Delete"])
def delete_dog(id):
    query = models.Dog.delete().where(models.Dog.id==id)
    query.execute()
    return jsonify(message='resource successfully deleted')







