from flask import Flask
from server_base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = Flask(__name__)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    users = session.query(User).all()
    return f'Users: {users}'

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)