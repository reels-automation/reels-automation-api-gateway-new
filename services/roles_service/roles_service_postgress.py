from roles_service import RolesService
from models.roles import Role
from server_base import Base, engine, Session

session = Session()

class RolesServicePostgress(RolesService):
    """_summary_

    Args:
        RolesService (_type_): _description_
    """

    def add_role(self, role_name: str):
        """_summary_

        Args:
            role_name (str): _description_
        """
        new_role = Role(
            name = role_name
        )
        session.add(new_role)
        session.commit()


    def delete_role(self):
        """_summary_
        """
        pass

    def update_role(self):
        """_summary_
        """
        pass
    
