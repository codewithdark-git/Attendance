from sqlalchemy import create_engine, Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import joblib
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(String, unique=True)
    program_name = Column(String)
    face_folder = Column(String)

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    subject = Column(String)
    date = Column(Date)

class Database:
    def __init__(self, db_path):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_user(self, name, user_id, program_name, face_folder):
        session = self.Session()
        new_user = User(name=name, user_id=user_id, program_name=program_name, face_folder=face_folder)
        session.add(new_user)
        session.commit()
        session.close()

    def save_attendance(self, program_name, subject, user_id, time, date):
        session = self.Session()
        attendance_record = Attendance(user_id=user_id, subject=subject, date=date)
        session.add(attendance_record)
        session.commit()
        session.close()

    def get_attendance(self, program_name, subject):
        session = self.Session()
        attendance_records = session.query(Attendance).filter_by(program_name=program_name, subject=subject).all()
        session.close()
        return attendance_records

    def load_model(self, program_name):
        model_path = f'models/{program_name}/face_recognition_model.pkl'
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            return None
