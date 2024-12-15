from uuid import uuid4
from utils.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, UUID, text

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, nullable=False, default=uuid4)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)

    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    is_deleted = Column(Boolean, default=False)

    def to_json(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": str(self.created_at)
        }