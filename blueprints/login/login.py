from flask import Blueprint, render_template, redirect, jsonify,request
from services.user_service.user_service_postgress import UserServicePostgress
from services.password_service.password_service_postgress import PasswordServicePostgress

login_blueprint = Blueprint("login", __name__)

@login_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print("Data: ", data)
    username = data["username"]
    password = data["password"]

    user_service_postgress = UserServicePostgress()
    password_service_postgress = PasswordServicePostgress()
    
    try:
        user_uuid = user_service_postgress.get_user_by_name(username)
        login = password_service_postgress.is_same_password(user_uuid, password)

        if login:
            return jsonify({"message: ": f"Congratulations {data["username"]} you are locked in"}), 201
        else:
            return jsonify({"message": f"kys"}),401

    except ValueError as e:
        print("Error: " , str(e))
        return jsonify({"message": f"Error: {str(e)}"}),404
