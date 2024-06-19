from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = 'sqlite:///attendance.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(String, unique=True)
    program_name = Column(String)
    faces = relationship('Face', back_populates='user')
    attendance = relationship('Attendance', back_populates='user')

class Face(Base):
    __tablename__ = 'faces'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    image_data = Column(String)
    user = relationship('User', back_populates='faces')

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subject = Column(String)
    date = Column(DateTime, default=datetime.now)
    user = relationship('User', back_populates='attendance')

def create_tables():
    Base.metadata.create_all(engine)