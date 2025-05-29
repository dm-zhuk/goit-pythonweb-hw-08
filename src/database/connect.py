from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from api.settings.base import DB_NAME

DB_URL = "sqlite:///.fast_api_project.db"

engine = create_engine(url=DB_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
