"""UserRolesServicePostgres.py
This module implements the UserRolesService interface for PostgreSQL database operations.

"""

from services.user_roles_service.user_roles_service import UserRolesService
from models.roles import UserRole
from server_base import Session

session = Session()

class UserRolesServicePostgres(UserRolesService):

    def create_user_role(self, role_uuid: str, user_uuid: str) -> str:
        new_role = UserRole(
            user_id = user_uuid,
            role_id = role_uuid
        )        
        session.add(new_role)
        session.commit()
        return new_role.id

    def get_role_from_user_uuid(self, user_uuid:str) -> UserRole:
        role = session.query(UserRole).filter_by(user_id=user_uuid).first()
        return role