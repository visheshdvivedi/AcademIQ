import datetime
from uuid import UUID
from validations import (
    validate_name,
    validate_email_address,
    validate_password
)

from pydantic import BaseModel, Field, field_validator

class CreateCourseSchema(BaseModel):
    name: str = Field(min_length=3, max_length=255, frozen=True)
    slug: str = Field(min_length=3, max_length=255)
    description: str

    instructor_id: UUID

    start_date: int
    end_date: int
    valid_till: int

    price: int
    available_slots: int
    total_slots: int

    @field_validator("start_date", "end_date", "valid_till")
    def validate_dates(cls, value):
        return datetime.datetime.fromtimestamp(value)