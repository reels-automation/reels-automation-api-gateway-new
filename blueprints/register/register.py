from flask import Blueprint, render_template, redirect, jsonify,request
from services.user_service.user_service_postgress import UserServicePostgress
from services.password_service.password_service_postgress import PasswordServicePostgress
from services.user_roles_service.user_roles_service_postgres import UserRolesServicePostgres
from services.roles_service.roles_service_postgress import RolesServicePostgress
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
    user_roles_service_postgres = UserRolesServicePostgres()
    roles_service_postgres = RolesServicePostgress()

    user_uuid = user_service_postgress.create_user(username, email)
    password_service_postgress.create_password(user_uuid,password)
    rol_id = roles_service_postgres.get_role_by_name("User")
    user_roles_service_postgres.create_user_role(rol_id,user_uuid)
    
    additional_claims = {
        "role": "User"  
    }

    access_token = create_access_token(identity=username,additional_claims=additional_claims)
    
    
    print("Data: ", data)
    return jsonify(access_token=access_token),201
