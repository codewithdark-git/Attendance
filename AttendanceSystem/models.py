from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = 'sqlite:///attendance.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    """
        User class represents the users table in the database.

        Attributes:
            id (int): Primary key of the user.
            name (str): Name of the user.
            user_id (str): Unique identifier of the user.
            program_name (str): Name of the program associated with the user.
            faces (relationship): Relationship to the Face class.
            attendance (relationship): Relationship to the Attendance class.
        """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    user_id = Column(String, unique=True)
    program_name = Column(String)
    faces = relationship('Face', back_populates='user')
    attendance = relationship('Attendance', back_populates='user')

class Face(Base):
    """
        Face class represents the faces table in the database.

        Attributes:
            id (int): Primary key of the face.
            user_id (int): Foreign key referencing the user ID.
            image_data (str): Base64 encoded image data of the face.
            user (relationship): Relationship to the User class.
        """
    __tablename__ = 'faces'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    image_data = Column(String)
    user = relationship('User', back_populates='faces')

class Attendance(Base):
    """
        Attendance class represents the attendance table in the database.

        Attributes:
            id (int): Primary key of the attendance record.
            user_id (int): Foreign key referencing the user ID.
            check_in_time (DateTime): Time when the user checked in.
            check_out_time (DateTime): Time when the user checked out.
            user (relationship): Relationship to the User class.
        """
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subject = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    user = relationship('User', back_populates='attendance')
    __table_args__ = (UniqueConstraint('user_id', 'subject', 'date', name='_user_subject_date_uc'),)

def create_tables():
    """
    Creates all the tables defined in the metadata of the `Base` class using the `engine` provided.

    This function is responsible for creating all the tables in the database that are defined in the metadata of the `Base` class. It uses the `create_all` method of the `Base.metadata` object to create all the tables.

    Parameters:
        None

    Returns:
        None
    """
    Base.metadata.create_all(engine)

create_tables()
