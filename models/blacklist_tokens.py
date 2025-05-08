import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Text
from database import Base

class BlacklistTokens(Base):
    __tablename__ = 'blacklist_tokens'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    bearer = Column(Text, nullable=False)