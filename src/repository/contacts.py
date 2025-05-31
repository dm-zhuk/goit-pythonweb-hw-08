"""Define functions for CRUD operations (to interact with DB) and search/birthday logic"""

from sqlalchemy.orm import Session
from database.models import Contact
from schemas.contact import ContactCreate, ContactUpdate
from datetime import date, timedelta


def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# offset(n) використовується для пропуску вказаної кількості рядків n перед поверненням результатів запиту
# skip — скільки записів потрібно пропустити з початку
# limit — кількість записів, що виводяться
def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.model_dump().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


# оператори для порівняння колонок зі значеннями або іншими колонками,такі як ==, !=, <, >, <=, >=, in_, like, ilike ..
# ilike => "case-Insensitive LIKE"
def search_contacts(db: Session, query: str):
    return (
        db.query(Contact)
        .filter(
            (Contact.first_name.ilike(f"%{query}%"))
            | (Contact.last_name.ilike(f"%{query}%"))
            | (Contact.email.ilike(f"%{query}%"))
        )
        .all()
    )


def get_upcoming_birthdays(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(Contact.birthday.between(today, next_week)).all()
