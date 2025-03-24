from services.user_service.user_service import UserService
from models.user import User
from server_base import Session

session = Session()

class UserServicePostgres(UserService):

    def create_user(self, username: str, email: str) -> str:
        """Inserta un registro de usuario a la base de datos de postgres

        Args:
            username (str)
            email (str)
        
        Return:
            new_user (str): el user creado
        """
        new_user = User(
            name = username,
            email = email
        )        
        session.add(new_user)
        session.commit()
        return new_user
    
    def get_user_by_name(self, username: str):
        """Obtiene un usuario en base a el nombre de usuario.

        Args:
            username (str): El nombre del usuario.
        """
        
        user = session.query(User).filter_by(name=username).first()
        
        return user.id
