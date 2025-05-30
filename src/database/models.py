from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .connect1 import Base, engine


class Owner(Base):
    __tablename__ = "owners"
    id = Base.Column(Base.Integer, primary_key=True, index=True)
    email = Column(String(150), nullable=False, unique=True, index=True)
    password = Column(String(128), nullable=False, index=True)
    first_name = Column(String(128), nullable=False, index=True)
    last_name = Column(String(128), nullable=False, index=True)


class Cat(Base):
    __tablename__ = "cats"
    id = Base.Column(Base.Integer, primary_key=True, index=True)
    nickname = Column(String(128), index=True)
    age = Column(Integer, index=True)
    is_vaccinated = Column(Boolean, index=True)
    description = Column(String(300), index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=True, index=True)
    owner = relationship("Owner", back_populates="cats")

    __table_args__ = (
        CheckConstraint("age >= 0", name="check_age_positive"),
        {"sqlite_autoincrement": True},
    )


Base.metadata.create_all(bind=engine)
