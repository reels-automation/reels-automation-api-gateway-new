from flask import Flask
from server_base import Base, engine
from models.user import User
from models.roles import Roles, UserRole
from models.passwords import UserPassword
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

Base.metadata.create_all(engine)

@app.route('/')
def index():
    return "Success"

if __name__ == '__main__':
    app.run(debug=True)