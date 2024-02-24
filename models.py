from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases
import os
from dotenv import load_dotenv

load_dotenv()  # This loads variables from .env into the environment
DATABASE_URL = os.getenv("DATABASE_URL")
database = databases.Database(DATABASE_URL)
Base = declarative_base()

# Example User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)


# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# SQLAlchemy sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
