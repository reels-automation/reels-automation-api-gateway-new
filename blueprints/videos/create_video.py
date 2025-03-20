from flask import Blueprint, render_template, redirect, jsonify,request
from services.user_service.user_service_postgress import UserServicePostgress
from services.password_service.password_service_postgress import PasswordServicePostgress
from services.user_roles_service.user_roles_service_postgres import UserRolesServicePostgres
from services.roles_service.roles_service_postgress import RolesServicePostgress
from flask_jwt_extended import create_access_token

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt

create_video_blueprint = Blueprint("create_video", __name__)

@create_video_blueprint.route("/create-video", methods=["GET"])
@jwt_required()
def create_video():
    token = get_jwt()

    if token["role"] != "Admin":
        return jsonify({"message": "No se puede crear el video. No sos admin"})

    return jsonify({"message":"Video creado correctamente"})