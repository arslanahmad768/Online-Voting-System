from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL Database URL

SQLACLHEMY_DATABASE_URL = "postgresql://postgres:usman786@localhost/ovs"

# Create a postgresql engine instance
engine = create_engine(SQLACLHEMY_DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Create a DeclarativeMeta instance
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()