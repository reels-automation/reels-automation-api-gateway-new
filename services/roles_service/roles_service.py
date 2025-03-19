from abc import ABC

class RolesService(ABC):

    def add_role(self, role_name: str):
        """Inserta un registro de rol o nivel de acceso en la tabla roles en la base de datos.
        Args:
            role_name (str): Nombre del rol
        """
        pass

    def delete_role(self):
        pass

    def update_role(self):
        pass
    