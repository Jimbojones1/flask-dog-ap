import models

import os
import sys
import secrets

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict
# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
user = Blueprint('users', 'user', url_prefix='/user')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # won't use f_name
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_fn)

    form_picture.save(file_path_for_avatar)

    # picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn )

@user.route('/register', methods=["POST"])
def register():
    ## see request payload anagolous to req.body in express
    payload = request.files

    pay = request.form.to_dict()

    dict_payload = payload.to_dict()
    print(payload, ' this is <-- payload')
    print(type(dict_payload['file']))
    print(pay['username'], ' this is pay?')
    print(pay)
    save_picture(dict_payload['file'])

    # payload['email'].lower()
    # try:
    #     # Find if the user already exists?
    #     models.User.get(models.User.email == payload['email'])
    #     return jsonify(body='User with that email already exists? Choose another or Login')
    # except models.DoesNotExist:
    #     payload['password'] = generate_password_hash(payload['password'])
    #     user = models.User.create(**payload)

    #     #login_user
    #     login_user(user)
    #     ## convert class Model to class dict
    #     user_dict = model_to_dict(user)
    #     print(user_dict)
    #     print(type(user_dict))
    #     # delete the password
    #     del user_dict['password']

    #     return jsonify(data=user_dict, status=201)
    return jsonify(message='working')

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










