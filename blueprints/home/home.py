from flask import Blueprint, render_template, redirect, jsonify,request
from services.user_service.user_service_postgres import UserServicePostgres
from services.password_service.password_service_postgres import PasswordServicePostgres
from flask_jwt_extended import create_access_token

home_blueprint = Blueprint("home", __name__)

@home_blueprint.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        try:
            return jsonify({"message": "Success"}), 201

        except Exception as e:
            print("Error: " , str(e))
            return jsonify({"message": f"Error Ineseperado.: {str(e)}"}), 404
