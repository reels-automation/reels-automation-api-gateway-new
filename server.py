""" Server """
import os

from flask import Flask
from flask_cors import CORS
from server_base import Base, engine
from sqlalchemy.orm import sessionmaker

from blueprints.home.home import home_blueprint
from blueprints.register.register import register_blueprint
from blueprints.login.login import login_blueprint
from blueprints.videos.create_video import create_video_blueprint

from flask_jwt_extended import JWTManager

from dotenv import load_dotenv

from utils.utils import create_default_roles

load_dotenv()

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
CORS(app)

JWT_KEY = os.getenv("JWT_KEY")

app.config["JWT_SECRET_KEY"] = JWT_KEY  
jwt = JWTManager(app)

app.register_blueprint(home_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(create_video_blueprint)

Base.metadata.create_all(engine)

create_default_roles()

if __name__ == '__main__':
    app.run(debug=True)
