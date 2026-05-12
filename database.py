import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Default to a local SQLite if Neon DB URL isn't set yet for testing
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./madhusiri.db")

# Neon requires sslmode=require if using psycopg2, but SQLAlchemy sometimes handles it differently.
# For SQLite, we need connect_args={"check_same_thread": False}.
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
