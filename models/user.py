import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Text, String
from server_base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(15), nullable=False)
    email = Column(Text, unique=True, nullable=False)
    
    password = relationship('UserPassword', back_populates='user')
    roles = relationship('Roles', secondary='user_roles', backref='users')

    def __repr__(self):
        return f'<User {self.name} - {self.email}>'