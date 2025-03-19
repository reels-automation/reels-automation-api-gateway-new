from flask import Flask
from server_base import Base, engine
from models.user import User
from models.roles import Roles, UserRole
from models.passwords import UserPassword
from sqlalchemy.orm import sessionmaker


from blueprints.helloworld.helloworld import helloworld_bp
from blueprints.register.register import register_blueprint
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

app.register_blueprint(helloworld_bp)
app.register_blueprint(register_blueprint)

Base.metadata.create_all(engine)


if __name__ == '__main__':
    app.run(debug=True)