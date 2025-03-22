from flask import Blueprint, render_template, redirect, jsonify,request
from services.user_service.user_service_postgres import UserServicePostgres
from services.password_service.password_service_postgres import PasswordServicePostgres
from flask_jwt_extended import create_access_token

login_blueprint = Blueprint("login", __name__)

@login_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print("Data: ", data)
    username = data["username"]
    password = data["password"]

    user_service_postgres = UserServicePostgres()
    password_service_postgres = PasswordServicePostgres()
    
    try:
        user_uuid = user_service_postgres.get_user_by_name(username)
        login = password_service_postgres.is_same_password(user_uuid, password)

        if login:
            access_token = create_access_token(identity=username)
            return jsonify(access_token), 201
        else:
            return jsonify({"message": f"Erorr. Credenciales Incorrectas."}),401

    except Exception as e:
        print("Error: " , str(e))
        return jsonify({"message": f"Error Ineseperado.: {str(e)}"}),404
