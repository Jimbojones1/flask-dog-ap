import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict
# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
user = Blueprint('users', 'user', url_prefix='/user')

@user.route('/register', methods=["POST"])
def register():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    payload['email'].lower()
    try:
        # Find if the user already exists?
        models.User.get(models.User.email == payload['email'])
        return jsonify(body='User with that email already exists? Choose another or Login')
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)

        #login_user
        login_user(user)
        ## convert class Model to class dict
        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        # delete the password
        del user_dict['password']

        return jsonify(data=user_dict, status=201)

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()

    try:
        user = models.User.get(models.User.email== payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            print(user, ' this is user')
            return jsonify(data=user_dict, status=200)
        else:
            return jsonify(data="Username or password does not Exist", status=200)
    except models.DoesNotExist:
        return jsonify(data="Username or password does not Exist", status=200)


@user.route('/profile/<id>', methods=['GET'])
def profile(id):
    try:
        user = models.User.get(models.User.id == id)
        user_dict = model_to_dict(user)
        del user_dict['password']
        return jsonify(data=user_dict)
    except models.DoesNotExist:
        return jsonify(data="User does not exist", status=200)










