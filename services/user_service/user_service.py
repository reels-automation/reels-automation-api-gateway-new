"""UserService Interface
This is an interface for the UserService class. It defines the methods that any implementation of the UserService class must have.
This interface is designed to be used with a PostgreSQL database, but it can be adapted for other databases as well.

"""

from abc import ABC

class UserService(ABC):

    def create_user(self):
        pass
    
    def update_user(self):
        pass

    def delete_user(self):
        pass

    def get_user(self):
        pass

    def get_user_by_name(self):
        pass

    def get_all_users(self):
        pass


