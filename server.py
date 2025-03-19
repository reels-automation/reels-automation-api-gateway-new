from flask import Flask
from server_base import Base, engine
from models.user import User
from models.roles import Roles, UserRole
from models.passwords import UserPassword
from sqlalchemy.orm import sessionmaker

# Create the session
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

Base.metadata.create_all(engine)

@app.route('/')
def index():
    users = session.query(User).all()
    return f'Users: {users}'

if __name__ == '__main__':
    app.run(debug=True)