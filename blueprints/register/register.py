from flask import Blueprint, render_template, redirect, jsonify,request
from services.user_service.user_service_postgress import UserServicePostgress



register_blueprint = Blueprint("register", __name__)

@register_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    email = data["email"]

    user_service_postgress = UserServicePostgress()
    user_service_postgress.create_user(username, email)

    print("Data: ", data)
    return jsonify({"message: ": f"Congratulations {data["username"]} you have an account"}), 201

