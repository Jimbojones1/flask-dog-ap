import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict
# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
user = Blueprint('users', 'user', url_prefix='/user')

@user.route('/', methods=["POST"])
def create_user():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    payload['password'] = generate_password_hash(payload['password'])
    user = models.User.create(**payload)

    #login_user
    login_user(user)
    ## see the object
    print(current_user, ' currentUser')
    user_dict = model_to_dict(user)
    print(user_dict)
    print(user.__dict__)
    print(type(user_dict))
    print(user)
    # delete the password
    del user_dict['password']
    ## Look at all the methods
    # print(dir(user))
    # Change the model to a dict
    # print(model_to_dict(user), 'model to dict')
    # return jsonify(message='working')
    return jsonify(user_dict)
