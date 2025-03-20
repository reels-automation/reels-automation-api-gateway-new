from flask import Blueprint, render_template, redirect, jsonify,request
from services.user_service.user_service_postgress import UserServicePostgress
from services.password_service.password_service_postgress import PasswordServicePostgress
from flask_jwt_extended import create_access_token


register_blueprint = Blueprint("register", __name__)

@register_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]

    user_service_postgress = UserServicePostgress()
    password_service_postgress = PasswordServicePostgress()
    user_uuid = user_service_postgress.create_user(username, email)
    password_service_postgress.create_password(user_uuid,password)

    access_token = create_access_token(identity=username)
    print("Data: ", data)
    return jsonify(access_token=access_token),201
