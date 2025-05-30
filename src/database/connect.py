from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.settings.base import DB_USER, DB_PASSWORD, DB_DOMAIN, DB_NAME, DB_PORT

# Database connection details
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_DOMAIN}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(url=DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Dependency to get DB session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
