import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Text, ForeignKey
from server_base import Base
from sqlalchemy.orm import relationship

class Roles(Base):
    __tablename__ = 'roles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(Text, nullable=False)

    def __repr__(self):
        return f'Rol: {self.name}'
    
class UserRole(Base):
    __tablename__ = 'user_roles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE'))

    def __repr__(self):
        return f'<UserRole user_id={self.user_id} role_id={self.role_id}>'