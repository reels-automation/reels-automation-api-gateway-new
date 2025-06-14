import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Text, String, Numeric
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    """User ORM class

    Args:
        id: UUID
        name:(str)
        email:(str)


    Returns:
        _type_: _description_
    """

    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    name = Column(String(15), nullable=False)
    email = Column(Text, unique=True, nullable=False)
    credits = Column(Numeric, default=1)

    password = relationship("UserPassword", back_populates="user")

    def __repr__(self):
        return f"<User {self.name} - {self.email}>"
