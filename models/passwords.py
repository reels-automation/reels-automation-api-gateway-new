import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Text, ForeignKey
from server_base import Base
from sqlalchemy.orm import relationship

class UserPassword(Base):
    __tablename__ = 'user_passwords'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    password_hash = Column(Text, nullable=False)

    user = relationship('User', back_populates='password')

    def __repr__(self):
        return f'<Hash=boiler>'