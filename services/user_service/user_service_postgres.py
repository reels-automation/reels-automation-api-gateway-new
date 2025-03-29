"""UserServicePostgres
Esta clase es la implementacion de la interfaz UserService para postgres.
Sirve para crear y obtener usuarios de la base de datos Postgres.
Esta clase utiliza SQLAlchemy para interactuar con la base de datos.
    Returns:
        _type_: _description_
"""
from services.user_service.user_service import UserService
from models.user import User
from server_base import Session

session = Session()

class UserServicePostgres(UserService):

    def create_user(self, username: str, email: str) -> User:
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
    
    def get_user_by_name(self, username: str) -> User:
        """Obtiene un usuario en base a el nombre de usuario.

        Args:
            username (str): El nombre del usuario.
        """
        
        user = session.query(User).filter_by(name=username).first()
        
        return user

    def get_user_credits(self, username:str) -> int:
        """Obtiene los creditos que tiene un usuario

        Args:
            username (str): nombre del usuario

        Returns:
            int: Cantidad de creditosdel usuario
        """
        
        user = self.get_user_by_name(username)
        return user.credits

    def can_make_post(self, username:str)-> bool:

        return self.get_user_credits(username) > 0

    def decrease_user_token(self, username:str):
        user = self.get_user_by_name(username)

        if user and user.credits > 0:
            user.credits -= 1
            session.commit()
            session.refresh(user)