""" utils """
from models.roles import Roles
from server_base import Session

session = Session()

def create_default_roles():
    required_roles = ["Admin", "User"]
    existing_roles = {role.name for role in session.query(Roles).all()}
    
    for role_name in required_roles:
        if role_name not in existing_roles:
            new_role = Roles(name=role_name)
            session.add(new_role)
    
    session.commit()