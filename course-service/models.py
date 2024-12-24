from uuid import uuid4
from utils.database import Base

from sqlalchemy import types
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, UUID, text, CheckConstraint

class Course(Base):
    __tablename__ = "courses"

    # basic information
    id = Column(UUID, primary_key=True, nullable=False, default=uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    is_deleted = Column(Boolean, default=False)

    # instructor information
    instructor_id = Column(UUID, nullable=False)
    instructor_name = Column(String, nullable=False)

    # course duration
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    valid_till = Column(TIMESTAMP(timezone=True), nullable=False)

    # pricing data
    price = Column(Integer, default=0)

    # student details
    available_slots = Column(Integer, default=0)
    total_slots = Column(Integer, default=50)

    # rating details
    rating = Column(Integer, default=3)

    __table_args__ = (
        CheckConstraint(
            "rating IN (1, 2, 3, 4, 5)", name='check_course_rating'
        ),
    )

    def to_json(self):
        return {
            # basic details
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "created_at": self.created_at,

            # instructor details
            "instructor_id": self.instructor_id,
            "instructor_name": self.instructor_name,

            # course duration details
            "start_date": self.start_date,
            "end_date": self.end_date,
            "valid_till": self.valid_till,

            # course pricing
            "price": self.price,

            # course available slots
            "available_slots": self.available_slots,
            "total_slots": self.total_slots,

            # course rating
            "rating": self.rating
        }