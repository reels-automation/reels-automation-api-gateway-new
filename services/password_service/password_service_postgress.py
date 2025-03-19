from services.user_service.user_service import UserService
from models.passwords import UserPassword
from server_base import Session

from werkzeug.security import generate_password_hash

session = Session()

class PasswordServicePostgress(UserService):

    def create_password(self, user_id:str, password:str):
        """_summary_

        Args:
            user_id (str): uuid of the user
            password (str): Non Hashed password
        """

        hashed_password = generate_password_hash(password)

        new_password = UserPassword(
            user_id = user_id,
            password_hash = hashed_password
        )

        session.add(new_password)
        session.commit()
