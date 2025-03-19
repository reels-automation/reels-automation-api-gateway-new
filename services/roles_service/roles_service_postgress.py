from roles_service import RolesService
from models.roles import Role
from server_base import Base, engine, Session

session = Session()

class RolesServicePostgress(RolesService):

    def add_role(self, role_name: str):
        new_role = Role(
            name = role_name
        )
        session.add(new_role)
        session.commit()


    def delete_role(self):
        pass

    def update_role(self):
        pass
    
