import models

import os
import sys
import secrets

from PIL import Image
from flask import Blueprint, request, jsonify, url_for, send_file
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

    output_size = (125, 175)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.rotate(30)
    i.save(file_path_for_avatar)

    return picture_fn
    # picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn )

@user.route('/register', methods=["POST"])
def register():
    ## see request payload anagolous to req.body in express
    ## This is how you get the image you sent over
    pay_file = request.files

    ## This has all the data like username, email, password
    payload = request.form.to_dict()
    dict_file = pay_file.to_dict()


    payload['email'].lower()
    try:
        # Find if the user already exists?
        models.User.get(models.User.email == payload['email'])
        return jsonify(data='User with that email already exists? Choose another or Login')
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        file_picture_path = save_picture(dict_file['file'])
        payload['image'] = file_picture_path
        user = models.User.create(**payload)


        #login_user
        login_user(user)

        current_user.image = file_picture_path
        ## convert class Model to class dict
        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        # delete the password
        del user_dict['password']

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()

    try:
        user = models.User.get(models.User.email== payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            print(user, ' this is user')
            return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})


@user.route('/profile/<id>', methods=['GET'])
def profile(id):
    try:
        user = models.User.get(models.User.id == id)
        user_dict = model_to_dict(user)
        del user_dict['password']
        return jsonify(data=user_dict, status={"code": 200, "message": "success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "User does Not Exist"})










