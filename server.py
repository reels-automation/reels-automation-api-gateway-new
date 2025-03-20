""" Server """
from flask import Flask
from server_base import Base, engine
from sqlalchemy.orm import sessionmaker

from blueprints.helloworld.helloworld import helloworld_bp
from blueprints.register.register import register_blueprint
from blueprints.login.login import login_blueprint

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

app.register_blueprint(helloworld_bp)
app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)

Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)
