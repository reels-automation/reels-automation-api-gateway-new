from services.user_roles_service.user_roles_service import UserRolesService
from models.roles import Roles
from server_base import Session

session = Session()

class UserRolesServicePostgres(UserRolesService):

    def create_user_role(self, role_uuid: str, user_uuid: str) -> str:
        new_role = Roles(
            role_id = role_uuid,
            user_id = user_uuid
        )        
        session.add(new_role)
        session.commit()
        return new_role.id
    
    def get_role_by_name(self, role: str):
        user = session.query(Roles).filter_by(name=role).first()
        
        return user.id
