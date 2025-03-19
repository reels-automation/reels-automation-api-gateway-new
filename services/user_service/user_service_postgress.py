from services.user_service.user_service import UserService
from models.user import User
from server_base import Session

session = Session()

class UserServicePostgress(UserService):

    def create_user(self, username: str, email: str) -> str:
        """Inserta un registro de usuario a la base de datos de postgress

        Args:
            username (str)
            email (str)
        
        Return:
            new_user.id (str): uuid del user
        """
        new_user = User(
            name = username,
            email = email
        )        
        session.add(new_user)
        session.commit()
        return new_user.id
