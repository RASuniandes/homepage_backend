from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import JSON

Base = declarative_base()

class Member(Base):
  __tablename__ = 'members'

  id = Column(String(36), primary_key=True)
  name = Column(String(255), nullable=False)
  email = Column(String(255), nullable=False, unique=True)
  role = Column(String(100), nullable=True)
  major = Column(String(255), nullable=False)
  double_major = Column(String(255), nullable=True)
  u_code = Column(String(50), nullable=True)
  phone_number = Column(String(20), nullable=True)
  project = Column(String(255), nullable=True)
  photo = Column(String(500), nullable=True)
  is_accepted = Column(Boolean, default=False)
  
  contributions = Column(JSON, nullable=True)
  skills = Column(JSON, nullable=True)
  goals = Column(JSON, nullable=True)
  
  is_in_council = Column(Boolean, default=False)
  join_date = Column(DateTime, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)