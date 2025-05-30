from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# Define shared fields for a contact
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr  # Ensure email is valid
    phone_number: Optional[str] = None
    birthday: Optional[date] = None
    additional_data: Optional[str] = None


# for creating/updating contacts
class ContactCreate(BaseModel):
    pass


class ContactUpdate(BaseModel):
    pass


# to return data, incl. id
class ContactResponse(BaseModel):
    id: int

    class Config:
        orm_mode = True  # allows pydantic to convert sqlalchemy objects to JSON
