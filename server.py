""" Server """
import os

from flask import Flask
from server_base import Base, engine
from sqlalchemy.orm import sessionmaker

from blueprints.helloworld.helloworld import helloworld_bp
from blueprints.register.register import register_blueprint
from blueprints.login.login import login_blueprint

from flask_jwt_extended import JWTManager

from dotenv import load_dotenv

from utils.utils import create_default_roles

load_dotenv()

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

JWT_KEY = os.getenv("JWT_KEY")

app.config["JWT_SECRET_KEY"] = JWT_KEY  
jwt = JWTManager(app)

app.register_blueprint(helloworld_bp)
app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)

create_default_roles()

Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)
