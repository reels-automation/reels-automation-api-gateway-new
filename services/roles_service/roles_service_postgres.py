"""RolesServicePostgres
This module provides an implementation of the RolesService for PostgreSQL.
It includes methods to add, delete, update, and retrieve roles from the database.

    Returns:
        _type_: _description_
"""
from services.roles_service.roles_service import RolesService
from models.roles import Roles
from server_base import Base, engine, Session

session = Session()

class RolesServicePostgres(RolesService):
    """_summary_

    Args:
        RolesService (_type_): _description_
    """

    def add_role(self, role_name: str):
        """_summary_

        Args:
            role_name (str): _description_
        """
        new_role = Roles(
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
    
    def get_role_by_name(self, role: str):
        user = session.query(Roles).filter_by(name=role).first()    
        return user.id
    
    def get_role_name_by_uuid(self, uuid:str)-> str:
        role = session.query(Roles).filter_by(id=uuid).first()
        return role.name

    def get_premium_roles(self):
        return ["Admin"]
