from sqlalchemy import create_engine, Column, Integer, String, DateTime, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
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
    email = Column(String, index=True)
    phone = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    created_at_v2 = Column(DateTime(timezone=True))
    session_id = Column(String)
    referer = Column(String)
    ip_address = Column(String)


class ClickEvent(Base):
    __tablename__ = "click_events"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(SmallInteger, index=True)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    timestamp_v2 = Column(DateTime(timezone=True))
    session_id = Column(String)
    ip_address = Column(String)
    
# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# SQLAlchemy sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
