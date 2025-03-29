"""PasswordServicePostgres
Esta clase es una implementación de la interfaz PasswordService.
Sirve para crear y verificar contraseñas de usuarios en una base de datos Postgres.
Esta clase utiliza SQLAlchemy para interactuar con la base de datos y Werkzeug para el hashing de contraseñas.
"""

from services.user_service.user_service import UserService
from models.passwords import UserPassword
from server_base import Session

from werkzeug.security import generate_password_hash, check_password_hash

session = Session()

class PasswordServicePostgres(UserService):
    def create_password(self, user_id:str, password:str):
        """Crea un hash de la contraseña de un nuevo usuario.

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

    def __get_password_by_user(self, user_uuid:str):
        """Devuelve la contraseña de un determinado usuario.

        Args:
            user_id (str): El usuario.
        """
        hashed_password = session.query(UserPassword).filter_by(user_id=user_uuid).first()

        return hashed_password.password_hash

    def is_same_password(self, user_id:str, password: str)-> bool:
        """Chequea si la contraseña dada por un usuario es la misma que la guardada.

        Args:
            user_id (str): El usuario.
            password (str): La contraseña sin hashear.
        """
        user_password = self.__get_password_by_user(user_id)

        return check_password_hash(user_password, password)
            


