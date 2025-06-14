"""Interfaz para crear contraseñas de usuarios y verificar si son iguales."""

from abc import ABC


class PasswordService(ABC):

    def create_password(self):
        pass

    def is_same_password(self):
        pass
