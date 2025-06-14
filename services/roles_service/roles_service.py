"""RolesService Interface"""

from abc import ABC


class RolesService(ABC):

    def add_role(self, role_name: str):
        """Inserta un registro de rol o nivel de acceso en la tabla roles en la base de datos.
        Args:
            role_name (str): Nombre del rol
        """

    def delete_role(self, role_id: str):
        pass

    def update_role(self, role_id: str, new_role_name: str):
        pass

    def get_role(self, role_id: str):
        """_summary_

        Args:
            role_id (str): _description_
        """
        ""
        pass
